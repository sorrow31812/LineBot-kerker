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


def googleSearch(keyword):
    # keyword = sys.argv
    google_url = 'https://www.google.com.tw/search'
    # search param
    my_params = {'q': keyword}
    req = requests.get(google_url, params=my_params)
    # Check status code
    if req.status_code == requests.codes.ok:
        bsParsingResult = BeautifulSoup(req.text, "html.parser")
        # print(bsParsingResult)
        # CSS selector
        selectionResult = bsParsingResult.select('div.g > h3.r > a[href^="/url"]')
        result_list = ''
        for idx, item in enumerate(selectionResult):
            # print(idx)
            # print("標題：" + item.text)
            url = item.get('href')
            urlResult = parseUrl(url)
            # print("網址：" + urlResult)
            result_list += '{}\n{}\n\n'.format(item.text, urlResult)
            if idx == 3:
                break
        # print(result_list)
        return result_list
    else:
        print(req.status_code)
        return 0


if __name__ == '__main__':
    googleSearch()
