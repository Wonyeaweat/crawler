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
baseurl = "http://news.scut.edu.cn"
visitedUrlSet = set(baseurl)
findLink = re.compile(r'href="(.*?)"')  # 正则表达式匹配链接
MAX_DEPTH = 3  # 最大层级为3


def main():
    fileName = "urls.txt"
    file = open(fileName, "w", encoding="UTF-8")  # 使用a+表示追加写
    file.close()
    urlQueue.put((baseurl, 0))  # 队列里包含形如 (url,depth) 的tuple元组
    while not urlQueue.empty():  # 待处理队列非空
        front = urlQueue.get()  # 取出队首待处理url数据
        urllist = getUrl(front)
        # print(urllist)
        for url in urllist:
            # print(url)
            if url not in visitedUrlSet:
                urlQueue.put(url)
                visitedUrlSet.add(url)
    # for i in range(1, 293):
    #    print("page", i)
    #    datalist = getData(baseurl + "41/list" + str(i) + ".htm")
    # savepath = ".\\covid19news.xls"
    # saveData(savepath)


def getUrl(front):
    print(front)
    nowUrl = str(front[0])  # 从（url,depth)中拆分出url 和 depth
    depth = int(front[1])
    urllist = []
    html = askURL(nowUrl)  # 获取了指定的网页信息
    soup = BeautifulSoup(html, "html.parser")
    title = str(soup.find("title"))

    '''fileName = './html/'+''.join(re.findall('[\u4e00-\u9fa5]', title)) + ".html"
    htmlfile = open(fileName, "w", encoding='utf-8')
    htmlfile.write(html)
    htmlfile.close()
    '''

    for item in soup.find_all('div'):
        item = str(item)
        link = re.findall(findLink, item)
        for ilink in link:
            if len(ilink) < 1:
                continue
            if ilink[0] != '/' and ilink[0] != 'h':
                continue
            if ilink[0] == '/':  # 相对地址
                ilink = baseurl + ilink
            if ilink not in visitedUrlSet and depth <= MAX_DEPTH:  # 层级小于最大值时 且未被访问过 才会添加URL
                urllist.append((ilink, depth + 1))
    return urllist


def askURL(url):  # 得到指定URL的网页信息
    head = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:88.0) Gecko/20100101 Firefox/88.0 "
                      "SCUTNIR2021S201836590301 "
    }  # 伪装浏览器请求头 注意该Key值是没空格的，不可写成 User - Agent
    request = urllib.request.Request(url, headers=head)
    html = ""
    try:
        url = quote(url, safe=string.printable)
        response = urllib.request.urlopen(url, timeout=10)
        # result = json.loads(result)
        # response = urllib.request.urlopen(request)
        # print(response.getcode())
        # html = ungzip(response.read()).decode("utf-8")
    except urllib.error.URLError as e:
        # 捕获异常 输出错误代码和原因
        if hasattr(e, "code"):
            print(e.code)
        if hasattr(e, "reason"):
            print(e.reason)
    else:
        fileName = "urls.txt"
        file = open(fileName, "a+", encoding="UTF-8")  # 使用a+表示追加写
        file.write(
            url + " " + str(response.getcode()) + " " + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f') + "\n")
        file.close()
        html = response.read().decode('utf-8', 'ignore').replace(u'\xa9', u'')
    return html


if __name__ == "__main__":
    main()
    # articleAnalyze(testarticleurl)
