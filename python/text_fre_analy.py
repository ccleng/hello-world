#分析云麓园BBS水吧文本,生成词频统计（单词和单词的频次）
import jieba
import csv

file = "text_ana_result.csv"
path = r'D:\Python\code\text_analy\云麓水吧.txt'

#with open(file,'w',newline='', encoding='utf-8') as csvfile:
with open(file,'w',newline='') as csvfile:
    writer = csv.writer(csvfile)

    read_txt = open(path, 'r')
    ShuiBa_word_list = []
    ShuiBa_word_set = set()
    for line in read_txt.readlines():
        line = line.replace(' ', '')
        line = line.strip('\n')
        word_list = jieba.lcut(line, cut_all=False)  #cut_all=false精准模式
        word_set = set(word_list)
        # 汇总水吧的所有词语的列表（有顺序，重复）
        ShuiBa_word_list = ShuiBa_word_list + word_list
        # 得到水吧所有词语的集合（无顺序，不重复）
        ShuiBa_word_set = ShuiBa_word_set.union(word_set)

    for word in ShuiBa_word_set:
        fre = ShuiBa_word_list.count(word)
        writer.writerow([word, str(fre)])





