import asyncio

import nest_asyncio

nest_asyncio.apply()
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

import requests
from aiohttp import ClientSession
from bs4 import BeautifulSoup
from lxml import etree

url = "https://www.xbiquge.so/book/55101/"
headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/98.0.4758.102 Safari/537.36 Edg/98.0.1108.62",
    "referer": "https://www.xbiquge.so/wanben/",
}


def saveFile(html, name, dir):
    text = getContent(html)
    path = Path(dir).joinpath(name + ".txt")
    path.write_text(text, encoding="gbk", errors="ignore")
    # print(name, "finish!!!")


def getContent(html):
    root = BeautifulSoup(html, "lxml")
    text = root.find("div", id="content").get_text("\n")
    return text.replace("&nbsp;", "")


def getUrl(url):
    with requests.get(url, headers=headers) as resp:
        resp.encoding = "gbk"
        tree = etree.HTML(resp.text)
        href = tree.xpath('//*[@id="list"]/dl/dd[position() >= 13]/a/@href')
        title = tree.xpath('//*[@id="list"]/dl/dd[position() >= 13]/a/text()')
    return href, title


async def getChapter(link, name):
    async with ClientSession() as session:
        async with session.get(link, headers=headers) as resp:
            return await resp.read(), name


async def getBook(url):
    href, title = getUrl(url)
    tasks = (
        asyncio.create_task(getChapter(url + id, name)) for id, name in zip(href, title)
    )
    return await asyncio.gather(*tasks)


def main():  # note:进程池必须位于__main__ 主进程中，必须可以被工作者子进程导入，最好用函数封装
    with ProcessPoolExecutor() as future:
        for html, name in htmls:
            future.submit(saveFile, html=html, name=name, dir="./download")


if __name__ == "__main__":
    htmls = asyncio.run(getBook(url))
    main()
