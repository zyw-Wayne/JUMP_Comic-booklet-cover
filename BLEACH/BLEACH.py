'''
Author: zyw_Wayne
Date: 2022-06-05 22:45:48
LastEditTime: 2022-10-10 00:31:22
'''

from lib2to3.pgen2 import driver
from bs4 import BeautifulSoup
from selenium import webdriver
from webdriver_manager.microsoft import EdgeChromiumDriverManager
import time
import json
import requests


def useDriver(url):  # 使用selenium获取页面

    opt = webdriver.EdgeOptions()
    # 浏览器无界面设置
    # opt.headless = True

    # 处理SSL证书错误问题
    opt.add_argument('--ignore-certificate-errors')
    opt.add_argument('--ignore-ssl-errors')

    # 忽略无用的日志
    opt.add_experimental_option(
        "excludeSwitches", ['enable-automation', 'enable-logging'])

    # 使用本地webdriver,存在安装失败、版本不同等问题
    # driver = webdriver.Edge(options=opt)

    # 使用在线自动获取webdriver
    driver = webdriver.Edge(EdgeChromiumDriverManager().install(), options=opt)
    driver.get(url)

    time.sleep(1)

    print('获取HTML')
    data = getHtmlText(driver)

    print('开始下载原图')
    isbn_list = data[0]
    download_original_img(isbn_list)  # 下载原图

    print('开始下载缩略图')
    # thumbnail_list = data[1]
    # download_thumbnail_img(thumbnail_list) # 下载缩略图

    print('操作结束退出程序')
    driver.quit()


def getHtml(url):  # 使用requests获取网页内容
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36 Edg/106.0.1370.37'
    }
    try:
        r = requests.get(url, headers=headers)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        return r.text
    except Exception:
        print('网络状态错误')


def getHtmlText(driver):
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')

    print('解析数据中>>>>>')
    all_script = soup.find_all('script')
    _list = all_script[13].get_text()
    _list = _list.split(";")[0].split("=")[1]
    _list = json.loads(_list)
    _list = _list['data']['item_datas']

    # 每个单行本的ISBN编码，用于单行本封面大图的下载
    isbn_list = []
    # 列表页单行本缩略图
    thumbnail_list = []

    for off in _list:
        isbn_list.append(
            {'name': off['item_name'], 'isbn': off['isbn']})
        thumbnail_list.append(
            {'name': off['item_name'], 'date': off['release_date'], 'url': off['image_url']})
    print('获取ISBN编码列表成功')
    print('获取缩略图列表成功')
    return [isbn_list, thumbnail_list]


def download_thumbnail_img(img_list):  # 下载每个单行本缩略图
    path = r'./thumbnail_imgs/'
    for l in img_list:
        name = l['name']
        date = l['date']
        file_path = path + name + '_' + date + '.jpg'

        with open(file_path, 'wb') as f, requests.get(l['url']) as res:
            f.write(res.content)
        print(f'{name}下载完成')


def download_original_img(isbn_list):  # 下载每个单行本的封面原图
    path = r'./original_imgs/'
    offprint_url = 'https://www.shueisha.co.jp/books/items/contents.html?isbn='
    # 比较可惜的是26卷的原图官方也是用的缩略图，差强人意啊
    for isbn in isbn_list:
        url = offprint_url+isbn['isbn']
        html = getHtml(url)
        img = get_offprint_img_url(html)
        name = isbn['name']
        file_path = path + name + '.jpg'
        time.sleep(1)
        with open(file_path, 'wb') as f, requests.get(img) as res:
            f.write(res.content)
        print(f'{name}下载完成')


def get_offprint_img_url(html):  # 获取每个单行本页面的图片url
    sp = BeautifulSoup(html, 'html.parser')
    itemimgs = sp.find('div', class_='itemimgs')
    img = itemimgs.find('img')
    return img.get('data-lazy')


def main():
    # 单行本列表url
    list_url = 'https://www.shueisha.co.jp/books/search/search.html?seriesid=35192&order=1'

    useDriver(list_url)


main()
