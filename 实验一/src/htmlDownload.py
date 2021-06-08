# -!- coding: utf-8 -!-
import string

import bs4  # 网页解析 获取数据
from bs4 import BeautifulSoup
import re  # 正则表达式
import urllib.request  # 制定URL，获取网页数据
import xlwt  # excel操作
import jieba.analyse
import gzip
import time
import queue
import importlib
import sys
import datetime
from urllib.parse import quote

importlib.reload(sys)


def ungzip(data):
    try:
        data = gzip.decompress(data)
    except:
        pass
    return data


# import _sqlite3        # SQL数据库操作
urlQueue = queue.Queue()
baseurl = "http://news.scut.edu.cn/"
visitedUrlSet = set(baseurl)
findLink = re.compile(r'href="(.*?)"')  # 正则表达式匹配链接
MAX_DEPTH = 3  # 最大层级为3

# http://news.scut.edu.cn/41/list + num + .htm
def main():
    for i in range(1, 293):
        print("page", i)
        getPage(baseurl + "41/list" + str(i) + ".htm")


def getPage(url):
    html = askURL(url)  # 获取了指定的网页的html
    soup = BeautifulSoup(html, "html.parser")
    for ilink in soup.find_all('div',id="wp_news_w45"):
        linklist = re.findall(findLink, str(ilink))
        for link in linklist:
            if link[0] == '/':# 相对路径
                link = baseurl+link
            savePage(link) # 保存对应网页的html

def savePage(url):
    html = askURL(url)
    soup = BeautifulSoup(html,"html.parser")
    title = str(soup.find("title"))
    fileName = './html/' + ''.join(re.findall('[\u4e00-\u9fa5]', title)) + ".html"  # 获取文章标题
    htmlfile = open(fileName, "w", encoding='utf-8')
    htmlfile.write(html)
    htmlfile.close()

def askURL(url):  # 得到指定URL的html
    head = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:88.0) Gecko/20100101 Firefox/88.0 "
                      "SCUTNIR2021S201836590301 "
    }  # 伪装浏览器请求头 注意该Key值是没空格的，不可写成 User - Agent
    request = urllib.request.Request(url, headers=head)
    html = ""
    try:
        url = quote(url, safe=string.printable)
        response = urllib.request.urlopen(url, timeout=10)
    except urllib.error.URLError as e:
        # 捕获异常 输出错误代码和原因
        if hasattr(e, "code"):
            print(e.code)
        if hasattr(e, "reason"):
            print(e.reason)
    else:
        html = response.read().decode('utf-8', 'ignore').replace(u'\xa9', u'')
    return html


if __name__ == "__main__":
    main()

