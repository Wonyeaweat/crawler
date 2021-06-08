import csv
import math
import sys
import os


def getIndex():  # 创建字典倒排索引
    csv.field_size_limit(500 * 1024 * 1024)  # 设置csv字段最大长度
    indexfile = open("./index.csv", "r")
    indexs = csv.reader(indexfile)
    index = {}
    for line in indexs:
        if len(line) > 1:
            key = line[0]  # '索引项'
            value = line[1:]  # []
            for i in range(len(value)):  # value[i] = '('编号'，'标题'，'链接'，tf词频)'
                value[i] = value[i][1:len(value[i]) - 1].replace('\'', '')  # value[i] = '编号,标题,链接,tf词频'
                value[i] = value[i].split(',')  # value[i] = ['编号', '标题', '链接','tf词频']
                value[i][0] = int(value[i][0])
                value[i][-1] = float(value[i][-1])
            index.update({key: value})
    '''
    index 是从index.csv里获取的倒排索引信息，构成一个字典
    注意，只有出现过该索引项的文章才会被记录（否则太多无用信息）
    index{
        '索引项':[[编号,'标题','链接',tf词频],[编号,'标题','链接',tf词频] ... ]
        '索引项':[[编号,'标题','链接',tf词频],[编号,'标题','链接',tf词频] ... ]
        ...    
    }
    '''
    return index


def takeSim(elem):
    return elem[1]


def solve(serachtext):
    index = getIndex()
    print("searching...")
    d = []  # 文档向量
    docid = set()  # 文档集编号
    hasword = dict()  # 记录 (文档编号,'索引项') : tf 信息
    outinfo = dict()  # 记录 文档编号 : ['标题', '链接'] 信息
    for word in serachtext:  # 枚举索引项
        textlist = index.get(word)
        '''
        textlist 是从倒排索引里获取得到的包含这个词的文章列表，构成一个list
        [[编号,'标题','链接',tf词频],[编号,'标题','链接',tf词频] ... ]
        '''
        # print(textlist)
        for text in textlist:  # 枚举每篇文章信息,是一个list [编号,'标题','链接',tf词频]
            if text[0] not in docid:
                docid.add(text[0])  # 加入文档集
                outinfo.update({text[0]: text[1:3]})
            hasword.update({(text[0], word): text[3]})

    for textid in docid:  # 枚举文档集文档编号 生成文档向量
        di = [textid]  # di = [文档编号，w_i,j, ... ]
        for word in serachtext:  # 枚举索引项
            n = len(index.get(word))  # 包含此索引项的文档个数
            idf = math.log(len(docid) / n)
            if (textid, word) in hasword:
                di.append(idf * hasword.get((textid, word)))
            else:
                di.append(0)
        d.append(di)

    q = []  # 查询向量
    for word in serachtext:  # 枚举索引项
        n = len(index.get(word))  # 包含此索引项的文档个数
        idf = math.log(len(docid) / n)
        q.append(idf)  # 注意分词后每个词出现1次，即 idf*(0.5 + 0.5*(1/1)) = idf

    sim = []  # 相似度结果列表 按相似度值降序排序
    for ditem in d:  # 枚举文档向量
        di = ditem[1:]
        sum = 0  # 内积法求相似度
        for i in range(len(q)):
            sum += q[i] * di[i]
        sim.append((ditem[0], sum))
    sim = sorted(sim, key=takeSim, reverse=True)
    # print(sim)
    # print(outinfo)
    print("-------------------result-------------------")
    for i in range(10):
        print("%d %s %s %f\n" % (1+i, outinfo[sim[i][0]][0],outinfo[sim[i][0]][1],sim[i][1]))

if __name__ == '__main__':
    usrinput = input("search: ").split(' ')
    print("loading data...")
    solve(usrinput)
