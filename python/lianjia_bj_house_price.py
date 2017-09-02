import csv
import re
from urllib.request import urlopen
from bs4 import BeautifulSoup

file = "lianjia_beijing_shunyi.csv"
#url = "http://bj.lianjia.com/ershoufang/changping/pg"
#url = "https://bj.lianjia.com/ershoufang/fengtai/pg"
url = "https://bj.lianjia.com/ershoufang/shunyi/pg"
#使用utf-8编码之后生成的excel打开时需要采用导入自文本数据的方式
with open(file,'w',newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)

    def house_scrap(house, writer):
        title = house.find("div",{"class":"title"}).a.string
        houseinfo = house.find("div",{"class":"houseInfo"}).text
        houseinfolist = houseinfo.split("|")
        neighbourhood = houseinfolist[0]
        layout = houseinfolist[1]
        square = houseinfolist[2]

        miscinfo = house.find("div",{"class":"flood"}).text
        miscinfolist = miscinfo.split("-")
        louceng = miscinfolist[0]
        xiaoqu = miscinfolist[1]

        details = house.find("div",{"class":"followInfo"}).text
        detaillist = details.split("/")
        detaillist_length = len(detaillist)
        guanzhu = None
        daikan = None
        fabushijian = None
        if detaillist_length == 1:
            guanzhu = re.sub("\D", "", detaillist[0])#提取数字
            #guanzhu = detaillist[0]
        elif detaillist_length == 2:
            #guanzhu = detaillist[0]
            guanzhu = re.sub("\D", "", detaillist[0])
            #daikan = detaillist[1]
            daikan = re.sub("\D", "", detaillist[1])
        elif detaillist_length == 3:
            #guanzhu = detaillist[0]
            guanzhu = re.sub("\D", "", detaillist[0])
            #daikan = detaillist[1]
            daikan = re.sub("\D", "", detaillist[1])
            fabushijian = detaillist[2]

        subway_ori = house.find("div", {"class":"tag"}).find("span", {"class":"subway"})
        if subway_ori != None:
            subway = subway_ori.text
        else:
            subway = None
        texfree_ori = house.find("div", {"class":"tag"}).find("span", {"class":"taxfree"})
        if texfree_ori != None:
            texfree = texfree_ori.text
        else:
            texfree = None
        haskey_ori = house.find("div", {"class":"tag"}).find("span", {"class":"haskey"})
        if haskey_ori != None:
            haskey = haskey_ori.text
        else:
            haskey = None

        price = house.find("div",{"class":"totalPrice"}).text
        per_price = house.find("div",{"class":"unitPrice"})["data-price"]#获取属性值
        #print(per_price)
        #per_price = house.find("div",{"class":"unitPrice"}).text

        #info.append(per_price)
        info = [title,neighbourhood,layout,square, louceng, xiaoqu, guanzhu, daikan, fabushijian, subway, texfree, haskey, price, per_price]

        writer.writerow(info)

    def page_scrap(url,writer):

        html = urlopen(url)
        bsObj = BeautifulSoup(html, "lxml")
        #print(bsObj.prettify())
        infos = bsObj.find("ul",{"class":"sellListContent"})
        for house in infos.findAll("li"):
            house_scrap(house,writer)

    for i in range(99):
        print(url+str(i+1))
        page_scrap(url+str(i+1),writer)    
