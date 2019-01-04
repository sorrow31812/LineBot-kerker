import sys
import requests
from urllib.parse import unquote
from bs4 import BeautifulSoup


def parseUrl(url):
    tempString = " " + url[7:]
    unneededParam = '&sa'
    unneededParamIndex = tempString.index(unneededParam)
    urlResult = tempString[:unneededParamIndex]
    result = unquote(urlResult)
    return result


def googleSearch():
    keyword = sys.argv
    google_url = 'https://www.google.com.tw/search'
    # search param
    my_params = {'q': keyword[1]}
    req = requests.get(google_url, params=my_params)
    # Check status code
    if req.status_code == requests.codes.ok:
        bsParsingResult = BeautifulSoup(req.text, "html.parser")
        # print(bsParsingResult)
        # CSS selector
        selectionResult = bsParsingResult.select('div.g > h3.r > a[href^="/url"]')
        for idx, item in enumerate(selectionResult):
            print(idx)
            # title
            print("標題：" + item.text)
            # url
            url = item.get('href')
            urlResult = parseUrl(url)
            print("網址：" + urlResult)
            if idx == 3:
                break
    else:
        print(req.status_code)


if __name__ == '__main__':
    googleSearch()
