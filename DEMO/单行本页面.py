'''
Author: zyw_Wayne
Date: 2022-05-29 22:25:42
LastEditTime: 2022-06-06 22:43:12
'''
from cgitb import html
import re
from turtle import ht
import requests
import os
from bs4 import BeautifulSoup
import urllib3

# 通过豆瓣死神页死神官方链接http://www.j-bleach.com/，获取每个单行本的封面图片


def getHtml(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.64 Safari/537.36 Edg/101.0.1210.53'
    }
    try:
        r = requests.get(url, headers=headers)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        return r.text
    except Exception:
        print('网络状态错误')


def getImgAndPageUrl(url):
    html = getHtml(url)

    soup = BeautifulSoup(html, 'html.parser')
    itemimgs = soup.find('div', class_='itemimgs')
    img = itemimgs.find('img')
    print(img.get('data-lazy'), img.get('alt'))

    return url


def fillPic(url):
    pic_url = getImgAndPageUrl(url)
    path = './BLEACH'


def main():

    url = 'https://www.shueisha.co.jp/books/items/contents.html?isbn=4-08-873213-8'  # 单行本1的链接地址
    if not os.path.exists('./BLEACH'):
        os.mkdir('./BLEACH/')

    fillPic(url)


main()

# https://www.shueisha.co.jp/books/search/search.html?seriesid=35192&order=1 死神所有单行本列表页
# https://www.shueisha.co.jp/books/search/search.html?seriesid=35181         火影忍者所有单行本列表页
# https://www.shueisha.co.jp/books/search/search.html?seriesid=34915         龙珠单行本列表页

# 因为死神的网站为日本网站，所以挂了梯子，但是访问的时候会报错
# 报错信息如下：EOF occurred in violation of protocol
# 解决方法见文章：https://pythonmana.com/2021/03/20210315220037740p.html
