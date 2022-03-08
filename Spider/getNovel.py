import asyncio
import random
import time

import aiohttp
import nest_asyncio

nest_asyncio.apply()
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

import requests
from aiohttp import ClientSession
from bs4 import BeautifulSoup
from faker import Faker
from lxml import etree


# 写入txt文本
def saveFile(html, name, dir):
    text = getContent(html)
    path = Path(dir).joinpath(name + ".txt")
    path.write_text('\n'.join((name, text)), encoding="gbk", errors="ignore")


# 解析html，提取小说内容
def getContent(html):
    root = BeautifulSoup(html, "lxml")
    text = root.find("div", id="content").get_text("\n")
    return text.replace("&nbsp;", "")


# 同步，获取章节链接、章节名
def getCatalogue(url):
    header = {"user-agent": fake.chrome()}
    with requests.get(url, headers=header) as resp:
        resp.encoding = "gbk"
        tree = etree.HTML(resp.text)
        href = tree.xpath('//*[@id="list"]/dl/dd[position() >= 13]/a/@href')
        title = tree.xpath('//*[@id="list"]/dl/dd[position() >= 13]/a/text()')
    pags = list(zip(href, title))
    random.shuffle(pags)
    return zip(*pags)


# 异步，获取章节页面
async def getChapter(link, referer):
    connector = aiohttp.TCPConnector(limit=30)  # 限制并发数量，使用aiohttp参数而不是asyncio.SemaPhore
    timeout = aiohttp.ClientTimeout(total=20)  # 程序应在total秒内完成，否则报超时错误
    header = {"user-agent": fake.chrome(), "referer": referer}
    async with ClientSession(connector=connector, timeout=timeout) as session:
        # await asyncio.sleep(1)
        async with session.get(link, headers=header) as resp:
            return await resp.read()
    # return html该位置返回值耗时最长


# 多阶段运行异步协程
async def getBook(url, href, num, offset):
    href = href[:num]
    for i in range(0, num, offset):
        began = time.time()
        tasks = (getChapter(url + id, book) for id in href[i: i + offset])
        chapters = await asyncio.gather(*tasks)  # note:不能塞入全部协程，否则服务器会拒绝访问，用循环划分
        over = time.time()
        count = min(num - i, offset)
        print(f"获取{count}个页面耗时{over - began}秒")
        htmls.extend(chapters)
        time.sleep(0.5)


# 多进程处理文本
def main(data, dir):  # note:进程池必须位于__main__ 主进程中，必须可以被工作者子进程导入，最好用函数封装
    with ProcessPoolExecutor() as future:
        for html, name in data:
            future.submit(saveFile, html=html, name=name, dir=dir)


if __name__ == "__main__":
    fake = Faker()  # 伪造user-agent
    book = f"https://www.xbiquge.so/book/4/"
    href, title = map(list, getCatalogue(book))
    htmls = list()  # 保存网页

    asyncio.run(getBook(book, href, len(href), 200))
    main(zip(htmls, title), "./novel")
