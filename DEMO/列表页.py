'''
Author: zyw_Wayne
Date: 2022-05-30 23:08:29
LastEditTime: 2022-06-01 14:16:16
'''
from cgitb import html
from cmath import log
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
    # 忽略证书
    # urllib3.disable_warnings()
    try:
        r = requests.get(url, headers=headers)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        return r.text
    except Exception:
        print('网络状态错误')


def getImgAndPageUrl(url):
    html = getHtml(url)
    print(html)
    # imgUrl = ''
    # nextPageUrl = ''
    # soup = BeautifulSoup(html, 'html.parser')
    # img = soup.find('img')
    # print(img)
    # nav = soup.find('nav', class_='item-btn-zenkan')
    # nextPage = nav.findChildren('li')
    # print(nextPage)

    return url


def getOffprintList(url):
    html = getHtml(url)
    print(html)
    # soup = BeautifulSoup(html, 'html.parser')
    # cards = soup.find('div', class_="card-outer")
    # print(cards)
    # singleItems = cards.find_all('section', class_='single-item')
    # print(singleItems)


def fillPic(url):
    # pic_url = getImgAndPageUrl(url)
    # offprintList = getOffprintList(url)
    # path = './BLEACH'

    getOffprintList(url)


def main():

    url = 'https://www.shueisha.co.jp/books/search/search.html?seriesid=35192&order=1'
    if not os.path.exists('./BLEACH'):
        os.mkdir('./BLEACH/')

    fillPic(url)


main()

# https://www.shueisha.co.jp/books/search/search.html?seriesid=35192&order=1 死神所有单行本列表页
# https://www.shueisha.co.jp/books/search/search.html?seriesid=35181         火影忍者所有单行本列表页

# 因为死神的网站为日本网站，所以挂了梯子，但是访问的时候会报错
# 报错信息如下：EOF occurred in violation of protocol
# 解决方法见文章：https://pythonmana.com/2021/03/20210315220037740p.html
