# -*- coding: utf-8 -*-
#https://thehackernews.com
#获取文章正文内容

import sys

import redis
import requests
import random
import time
from lxml import etree
from pymongo import MongoClient

my_headers = [    "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36",
                  "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.153 Safari/537.36",
                  "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:30.0) Gecko/20100101 Firefox/30.0",
                  "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.75.14 (KHTML, like Gecko) Version/7.0.3 Safari/537.75.14",
                  "Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Win64; x64; Trident/6.0)",
                  'Mozilla/5.0 (Windows; U; Windows NT 5.1; it; rv:1.8.1.11) Gecko/20071127 Firefox/2.0.0.11',
                  'Opera/9.25 (Windows NT 5.1; U; en)',
                  'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)',
                  'Mozilla/5.0 (compatible; Konqueror/3.5; Linux) KHTML/3.5.5 (like Gecko) (Kubuntu)',
                  'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.8.0.12) Gecko/20070731 Ubuntu/dapper-security Firefox/1.5.0.12',
                  'Lynx/2.8.5rel.1 libwww-FM/2.14 SSL-MM/1.4.1 GNUTLS/1.2.9',
                  "Mozilla/5.0 (X11; Linux i686) AppleWebKit/535.7 (KHTML, like Gecko) Ubuntu/11.04 Chromium/16.0.912.77 Chrome/16.0.912.77 Safari/535.7",
                  "Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:10.0) Gecko/20100101 Firefox/10.0 ",
                  'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
                  'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.67 Safari/537.36']
headers = {
    'user-agent': random.choice(my_headers),
    'Upgrade-Insecure-Requests': '1',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Enocding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9',
}


def get_article(url):
    print(url)
    retry = 3
    while retry > 0:
        try:
            page_source = requests.get(url, headers=headers, timeout=10).content
            retry = 0
        except:
            print("@@@@@@@@@@@@@@@@sleep@@@@@@@@@@@@@@")
            time.sleep(60)
            print("retry:" + " " + str(retry))
            retry = retry - 1
            if retry == 0:
                sys.exit(0)
    html = etree.HTML(page_source)
    title = html.xpath("//h1[@class='story-title']/a/text()")
    if len(title) > 0:
        title = title[0]
    else:
        title = ''
    article = html.xpath("//div[@id='articlebody']")
    article_text = ''
    for x in article:
        for eve_text in x.itertext():
            article_text = article_text + ' ' + eve_text

    dict = {
        'url': url,
        'title': title.encode('utf-8'),
        'article': article_text.encode('utf-8')
    }
    return dict

def save_mongo(dict):
    conn = MongoClient('127.0.0.1', 27017)
    db = conn.thehackernews
    my_set = db.article_1106_1757
    try:
        my_set.insert(dict)
        print('******************insert database success!*************************')
    except:
        print('###################insert database fail!!#######################')

def get_id_from_mongo():
    conn = MongoClient('127.0.0.1', 27017)
    db = conn.thehackernews
    my_set = db.list_1106_1718
    all_article = my_set.find()
    for article in all_article:
        print('----------------------------------------------------------------------------------------------------')
        dict = get_article(article['post_url'])
        save_mongo(dict)

def get_url_from_redis(url_list):
    pool = redis.ConnectionPool(host='localhost', port=6379, decode_responses=True)
    r = redis.Redis(connection_pool=pool)
    while r.llen(url_list) > 0:
        print('----------------------------------------------------------------------------------------------------')
        x = r.lpop(url_list)
        # if int(post_id) <= 8532:
        dict = get_article(x)
        save_mongo(dict)
        print('%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%')

if __name__ == '__main__':
    url_list = 'url'
    get_url_from_redis(url_list)