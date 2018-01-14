#!/usr/bin/env python
#-*- coding:utf-8 -*-
import csv
import re
from urllib.request import urlopen
from bs4 import BeautifulSoup

file = "lianjia_beijing_nanshatanxiaoqu_chengjiao.csv"
url_head = "https://bj.lianjia.com/chengjiao/"
url_page = "pg"
#永泰园
#url_tail = "rs%E6%B0%B8%E6%B3%B0%E5%9B%AD/"
#南沙滩小区
url_tail = "rs%E5%8D%97%E6%B2%99%E6%BB%A9%E5%B0%8F%E5%8C%BA/"
url_pg1 = "https://bj.lianjia.com/chengjiao/rs%E6%B0%B8%E6%B3%B0%E5%9B%AD/"
url_pg2 = "https://bj.lianjia.com/chengjiao/pg2rs%E6%B0%B8%E6%B3%B0%E5%9B%AD/"
#使用utf-8编码之后生成的excel打开时需要采用导入自文本数据的方式
with open(file,'w',newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)

    def house_scrap(house, writer):
        title = house.find("div",{"class":"title"}).a.string
        houseinfo = house.find("div",{"class":"houseInfo"}).text
        houseinfolist = houseinfo.split("|")
        houseinfo_length = len(houseinfolist)
        if houseinfo_length == 0:
            direction = None
            zhuangxiu = None
            dianti = None
        elif houseinfo_length == 1:
            direction = houseinfolist[0]
            zhuangxiu = None
            dianti = None
        elif houseinfo_length == 2:
            direction = houseinfolist[0]
            zhuangxiu = houseinfolist[1]
            dianti = None
        elif houseinfo_length == 3:
            direction = houseinfolist[0]
            zhuangxiu = houseinfolist[1]
            dianti = houseinfolist[2]
        print(title, houseinfo, direction, zhuangxiu, dianti)

        deal_date = house.find("div",{"class":"dealDate"}).text
        total_price_ori = house.find("div",{"class":"totalPrice"})
        if total_price_ori != None:
            total_price_o = total_price_ori.find("span",{"class":"number"})
            if total_price_o != None:
                total_price = total_price_o.text
            else:
                total_price = None
        else:
            total_price = None
        print(deal_date, total_price)

        floodinfo = house.find("div",{"class":"flood"})
        miscinfo = floodinfo.find("div",{"class":"positionInfo"}).text
        sourceinfo = floodinfo.find("div",{"class":"source"}).text
        unitprice_ori = floodinfo.find("div",{"class":"unitPrice"})
        if unitprice_ori != None:
            unitprice_o = unitprice_ori.find("span",{"class":"number"})
            if unitprice_o != None:
                unitprice = unitprice_o.text
            else:
                unitprice = None
        else:
            unitprice = None
        print(floodinfo, miscinfo, sourceinfo, unitprice)

        #deal_house_info = house.find("div",{"class":"dealHouseInfo"})
        #deal_house_txt = deal_house_info.find("span",{"class":"dealHouseTxt"}).find("span").text

        #dealCycleeinfo = house.find("div",{"class":"dealCycleeInfo"})
        #deal_cyclee_txt = dealCycleeinfo.find("span",{"class":"dealCycleTxt"}).find("span").text

        #info.append(per_price)
        #info = [title,direction,zhuangxiu,dianti, deal_date, total_price, miscinfo, sourceinfo, unitprice, deal_house_txt, deal_cyclee_txt]
        info = [title, direction, zhuangxiu, dianti, deal_date, total_price, miscinfo, sourceinfo, unitprice]

        writer.writerow(info)

    def page_scrap(url,writer):

        html = urlopen(url)
        bsObj = BeautifulSoup(html, "lxml")
        #print(bsObj.prettify())
        infos = bsObj.find("div", {"class": "content"}).find("div",{"class":"leftContent"}).find("ul",{"class":"listContent"})
        #print(infos)
        for house in infos.findAll("li"):
            house_scrap(house,writer)

    for i in range(24):
        j = i + 1
        if j == 1:
            url_full = url_head + url_tail
        else:
            url_full = url_head + url_page + str(j) + url_tail
        print(url_full)
        page_scrap(url_full,writer)
