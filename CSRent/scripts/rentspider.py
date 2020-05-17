# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
import csv

# num表示记录序号
Url_head = "http://fangzi.xmfish.com/web/search_hire.html?h=&hf=&ca=5920"
Url_tail = "&r=&s=&a=&rm=&f=&d=&tp=&l=0&tg=&hw=&o=&ot=0&tst=0&page="
Num = 0
Filename = "./data/rent.csv"


# 把每一页的记录写入文件中
def write_csv(msg_list):
    out = open(Filename, 'a', newline='')
    csv_write = csv.writer(out,dialect='excel')
    for msg in msg_list:
        csv_write.writerow(msg)
    out.close()


# 访问每一页
def acc_page_msg(page_url):
    web_data = requests.get(page_url).content.decode('utf8')
    soup = BeautifulSoup(web_data, 'html.parser')
    address_list = []
    area_list = []
    num_address = 0
    num_area = 0
    msg_list = []

    # 得到了地址列表，以及区域列表
    for tag in soup.find_all(attrs="list-addr"):
        for em in tag:
            count = 0
            for a in em:
                count += 1
                if count == 1 and a.string != "[":
                    address_list.append(a.string)
                elif count == 2:
                    area_list.append(a.string)
                    num_area += 1
                elif count == 4:
                    if a.string is not None:
                        address_list[num_address] = address_list[num_address] + "-" + a.string
                    else:
                        address_list[num_address] = address_list[num_address] + "-Null"
                    num_address += 1

    # 得到了价格列表
    price_list = []
    for tag in soup.find_all(attrs="list-price"):
        price_list.append(tag.b.string)

    # 组合成为一个新的tuple——list并加上序号
    for i in range(len(price_list)):
        txt = (address_list[i], area_list[i], price_list[i])
        msg_list.append(txt)

    # 写入csv
    write_csv(msg_list)


# 爬所有的页面
def get_pages_urls():
    urls = []
    # 思明可访问页数134
    for i in range(134):
        urls.append(Url_head + "1" + Url_tail + str(i+1))
    # 湖里可访问页数134
    for i in range(134):
        urls.append(Url_head + "2" + Url_tail + str(i+1))
    # 集美可访问页数27
    for i in range(27):
        urls.append(Url_head + "3" + Url_tail + str(i+1))
    # 同安可访问页数41
    for i in range(41):
        urls.append(Url_head + "4" + Url_tail + str(i+1))
    # 翔安可访问页数76
    for i in range(76):
        urls.append(Url_head + "5" + Url_tail + str(i+1))
    # 海沧可访问页数6
    for i in range(6):
        urls.append(Url_head + "6" + Url_tail + str(i+1))
    return urls


def run():
    print("开始爬虫")
    out = open(Filename, 'a', newline='')
    csv_write = csv.writer(out, dialect='excel')
    title = ("address", "area", "price")
    csv_write.writerow(title)
    out.close()
    url_list = get_pages_urls()
    for url in url_list:
        try:
            acc_page_msg(url)
        except:
            print("格式出错", url)
    print("结束爬虫")


