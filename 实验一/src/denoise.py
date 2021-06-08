import os
from bs4 import BeautifulSoup
import re

htmllist = []
def findAllFile(base):
    for root, ds, fs in os.walk(base):
        for f in fs:
            fullname = os.path.join(root, f)
            html = open(fullname,"r",encoding='utf-8')
            soup = BeautifulSoup(html,"html.parser")
            title = str(soup.find("title"))
            fileName = './denoise/' + ''.join(re.findall('[\u4e00-\u9fa5]', title)) + ".txt"
            print(fileName)
            txt = open(fileName,'w',encoding='utf-8')
            for item in soup.find_all('div', class_="entry"):
                item = str(item)
                articletext = ''.join(re.findall('[\u4e00-\u9fa5]', item))
                txt.write(articletext)
            txt.close()

def main():
    findAllFile("./html")

'''
def articleAnalyze(articleurl):
    # 进入指定的页面获取文章信息 判断与疫情是否相关
    if (articleurl[0] == '/'):
        articleurl = baseurl + articleurl
    html = askURL(articleurl)
    soup = BeautifulSoup(html, "html.parser")

    sim = 0
    for item in soup.find_all('div', class_="entry"):
        item = str(item)
        articletext = ''.join(re.findall('[\u4e00-\u9fa5]', item))
        # print(articletext)
        # 此时articletext是将文章内容提取了出来
    if (sim > 0.0):
        print(articleurl, sim)


def saveData(savepath):
    print("save....")
'''

if __name__ == "__main__":
    main()