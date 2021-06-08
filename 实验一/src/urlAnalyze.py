import numpy as np
import time
import matplotlib.pyplot as plt

data = []
def main():
    fileName = "url-raw.txt"
    file = open(fileName,"r",encoding='utf-8')
    # url.txt 是爬虫爬取url数据时的日志，格式为 url status_code date time
    # line = file.readline().split()
    # print(line,type(line))
    timelist = []
    for line in file.readlines():
        newline = line.split()# 按空格分开，将str划分成list
        t = time.mktime(time.strptime(newline[2] + ' ' + newline[3], '%Y-%m-%d %H:%M:%S.%f'))
        timelist.append(t)
    begtime = timelist[0]
    for i in range(len(timelist)): # 统计从爬虫开始爬取网页时过去的毫秒数
        timelist[i]-=begtime

    y = range(len(timelist))
    plt.plot(timelist,y)
    plt.xlabel('time')
    plt.ylabel('number of pages')
    plt.show() # 网页爬取数量 - 用时 折线图

if __name__ == "__main__":
    main()