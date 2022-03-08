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
    path.write_text("\n".join((name, text)), encoding="gbk", errors="ignore")


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
async def getChapter(link, referer, session):
    header = {"user-agent": fake.chrome(), "referer": referer}
    async with session.get(link, headers=header, timeout=60) as resp:  # with中的__exit__()会在return后执行
        return await resp.read()


# 多阶段运行异步协程
async def getBook(url, href):
    connector = aiohttp.TCPConnector(limit=100)  # 限制并发数量，使用aiohttp参数而不是asyncio.SemaPhore
    timeout = aiohttp.ClientTimeout(total=600)  # 程序应在total秒内完成，否则报超时错误
    async with ClientSession(connector=connector, timeout=timeout) as session:  # 一个client下的多个连接池
        began = time.time()
        tasks = (getChapter(url + id, book, session) for id in href)
        chapters = await asyncio.gather(*tasks)
        over = time.time()
    print(f"获取页面耗时{(over - began): .2f}秒")
    return chapters


# 多进程处理文本
def main(data, dir):  # note:进程池必须位于__main__ 主进程中，必须可以被工作者子进程导入，最好用函数封装
    with ProcessPoolExecutor() as future:
        for html, name in data:
            future.submit(saveFile, html=html, name=name, dir=dir)


if __name__ == "__main__":
    fake = Faker()  # 伪造user-agent
    book = f"https://www.xbiquge.so/book/4/"
    href, title = map(list, getCatalogue(book))

    htmls = asyncio.run(getBook(book, href))
    began = time.time()
    main(zip(htmls, title), "./novel")
    print(f'处理并写入文本耗时{(time.time() - began): .2f}秒')
