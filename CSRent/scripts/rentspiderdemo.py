import requests
from lxml import etree
import pandas as pd
import random


def rentSpider(region):
    max_page = 40
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',

        }
    # 设置代理
    proxies = [
        {'https': "https://221.6.201.18:9999"},
        {'http': 'http://39.137.69.9:80'},
        {'https': 'https://221.122.91.64:80'},
        {'http': 'http://39.137.69.8:8080'},
        {'http': 'http://125.59.223.27:8380'},
        {'http': 'http://118.212.104.22:9999'},
        {'https': 'https://47.106.59.75:3128'},
        {'http': 'http://221.180.170.104:8080'},
        {'http': 'http://113.59.99.138:8910'},
        {'http': 'http://123.194.231.55:8197'},
        {'https': 'https://218.60.8.99:3129'},
        {'http': 'http://218.58.194.162:8060'},
        {'https': 'https://221.122.91.64:80'}
    ]
    base_url = 'http://www.xhj.com/zufang/'
    tmp1 = []
    tmp2 = []
    for i in range(1, max_page + 1):
        url = base_url + region + '/pg%d/' % i
        while True:
            try:
                proxie = random.choice(proxies)
                r = requests.get(url, headers=header, proxies=proxie, timeout=1)
                if r.status_code == 200:
                    print('Response status code 200:' + url)

                    content = r.text
                    html = etree.HTML(content)
                    div = html.xpath('//*/div[@class="lp_wrap"]')

                    for i in range(len(div)):
                        price = div[i].xpath('div[2]/p[1]/span/text()')[0]
                        addr = (div[i].xpath('div[1]/div/text()')[5][1:]).strip('[\n\t\r ]')
                        tmp1.append(price)
                        tmp2.append(addr)
                    break
            except Exception as e:
                pass
            # print(e)

            finally:
                proxie = random.choice(proxies)

    return {
        'price': tmp1,
        'addr': tmp2,
    }

def run():
    print("开始爬虫...")
    # 天心区、芙蓉区、开福区、岳麓区、雨花区、望城
    param = ['tianxinqu','furongqu','kaifuqu','yueluqu','yuhuaqu','wangcheng']
    cn_par = ['天心区','芙蓉区','开福区','岳麓区','雨花区','望城']

    j = 0
    dt = pd.DataFrame(columns=['addr','area','price'])
    dt = dt[['addr','area','price']]
    for i in param:
        re = rentSpider(i)
        re['area'] = cn_par[j]
        j +=1
        tmp = pd.DataFrame(re)
        tmp = tmp[['addr','area','price']]
        dt = dt.append(tmp)

    dt.to_csv('./data/rent_info.csv',encoding='utf_8_sig',index=False)

    print("结束爬虫！")