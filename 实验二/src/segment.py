#coding:utf-8
import jieba
import csv
import jieba.posseg as psg

def stopwordslist():
    stopwords = [line.strip() for line in open('./stop.txt',encoding='UTF-8').readlines()]
    return stopwords

wordlist = set() # 创建词汇表

def seg_sentence(sentence):
    fopen = open("./wordlist.txt", "a+");
    sentence_depart = jieba.cut(sentence.strip())
    stopwords = stopwordslist()# 创建一个停用词列表
    global wordlist
    for word in sentence_depart:
        if word not in stopwords and word not in wordlist:
            wordlist.add(word)
            fopen.write(word+'\n')

def csvread(): # 读取csv文件
    csv.field_size_limit(500 * 1024 * 1024) # 设置csv字段最大长度

    with open('./data.csv') as f:
        f_csv = csv.reader(f)
        for row in f_csv:
            if len(row) > 1:
                sentence = row[3] # [No.?,url,title,text]
                print(row[0],row[2],len(wordlist))
                seg_sentence(sentence)
def main():
    csvread()


if __name__ == "__main__":
    main()
