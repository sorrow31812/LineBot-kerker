import concurrent.futures
import datetime
import os
import shutil
import sys
import time
from functools import partial

import requests
import urllib3
from bs4 import BeautifulSoup
import random

urllib3.disable_warnings()

rs = requests.session()


def over18(url):
    res = rs.get(url, verify=False)
    # 先檢查網址是否包含'over18'字串 ,如有則為18禁網站
    if 'over18' in res.url:
        print("18禁網頁")
        # 從網址獲得版名
        board = url.split('/')[-2]
        load = {
            'from': '/bbs/{}/index.html'.format(board),
            'yes': 'yes'
        }
        res = rs.post('https://www.ptt.cc/ask/over18', verify=False, data=load)
    return BeautifulSoup(res.text, 'html.parser'), res.status_code


# 移除特殊字元（移除Windows上無法作為資料夾的字元）
def remove(value, deletechars):
    for c in deletechars:
        value = value.replace(c, '')
    return value.rstrip()


def image_url(link):
    # 符合圖片格式的網址
    image_seq = ['.jpg', '.png', '.gif', '.jpeg']
    for seq in image_seq:
        if link.endswith(seq):
            return link
    # 有些網址會沒有檔案格式， "https://imgur.com/xxx"
    if 'imgur' in link:
        return '{}.jpg'.format(link)
    return ''


def download_link(directory, link):
    res_img = rs.get(link, stream=True, verify=False)
    # 使用網址的最後一個字串設為圖片檔案名稱
    filename = link.split('/')[-1]
    relative_path = os.path.join(directory, filename)
    path = os.path.abspath(relative_path)
    try:
        if not os.path.exists(path):
            with open(path, 'wb') as out_file:
                shutil.copyfileobj(res_img.raw, out_file)
            del res_img
    except Exception as e:
        print('shutil.copyfileobj error')


def store_pic(crawler_time, url, rate='', title=''):
    # 檢查看板是否為18禁,有些看板為18禁
    soup, _ = over18(url)
    # 避免有些文章會被使用者自行刪除標題列
    try:
        title = soup.select('.article-meta-value')[2].text
    except Exception as e:
        title = "no title"

    dir_name = '{}_{}'.format(remove(title, '\/:*?"<>|.'), rate)
    pic_url_list = []

    # 抓取圖片URL(img tag )
    for img in soup.find_all("a", rel='nofollow'):
        img_url = image_url(img['href'])
        if img_url:
            pic_url_list.append(img_url)

    # 開始建立資料夾,使用文章標題做為資料夾的名稱
    # page_number = random.randint(0, 15)
    url_list_len = len(pic_url_list)
    # print("Pic List length : " + str(url_list_len))
    # print(*pic_url_list, sep="\n")
    url_number = random.randint(0, url_list_len - 1)

    return pic_url_list[url_number]


def main():
    print("Analytical download page...")
    datetime_format = '%Y%m%d%H%M%S'
    crawler_time = '_PttImg_{:{}}'.format(datetime.datetime.now(), datetime_format)
    beauty_article_urls = []
    # 從.txt檔案中讀取 urls
    total = 0
    with open(sys.argv[1]) as fd:
        for url in fd:
            if 'www.ptt.cc' in url.strip():
                beauty_article_urls.append(url.strip())
                total += 1

    count = 0
    url = beauty_article_urls.pop(0)
    # 檢查看板是否為18禁,有些看板為18禁
    _, status_code = over18(url)
    # 如網頁忙線中,則先將網頁加入 index_list 並休息1秒後再連接
    if status_code != 200:
        beauty_article_urls.append(url)
        time.sleep(1)
    else:
        count += 1
        final_url = store_pic(crawler_time, url)
    time.sleep(0.05)

    return final_url


if __name__ == '__main__':
    main()
