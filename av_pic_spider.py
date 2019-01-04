import requests
from bs4 import BeautifulSoup
import random
import imgur_upload


def index_containing_substring(the_list, substring):
    for idx, i in enumerate(the_list):
        if str(i).find(substring) > 0:
            return idx
    return -1


def main():
    # keyword = sys.argv
    page_random = random.randint(400, 9707)
    target_url = 'http://18av.tv/cg_{}.html'.format(page_random)
    print(target_url)
    # search param
    cookies = {'javascript_cookie_Eighteenth': 'I_am_over_18_years_old'}
    req = requests.post(target_url, cookies=cookies)
    # Check status code
    if req.status_code == requests.codes.ok:
        bsParsingResult = BeautifulSoup(req.text, "html.parser")
        url_array = bsParsingResult.find_all("script")
        url_num = index_containing_substring(url_array, 'wbhost3')
        print(url_num)
        # with open("Output.txt", "w") as text_file:
        #     print(test.encode("utf8").decode("cp950", "ignore"), file=text_file)
        selectionResult = str(url_array[url_num])
        # print(selectionResult)
        # pic_jpg_index = 0
        pic_http_index = 0
        keyword_http = 'http'
        keyword_jpg = '.jpg'
        url_list = []
        while pic_http_index >= 0:
            pic_jpg_index = selectionResult.index(keyword_jpg)
            tmp = selectionResult[:pic_jpg_index+4]
            pic_http_index = tmp.index(keyword_http)
            img_url = tmp[pic_http_index:]
            url_list.append(img_url)
            selectionResult = selectionResult[pic_jpg_index+4:]
            pic_http_index = selectionResult.find(keyword_http)
    else:
        print(req.status_code)

    # print(*url_list, sep="\n")
    url_random = random.randint(1, len(url_list))
    final_url = imgur_upload.main(url_list[url_random])
    return final_url


if __name__ == '__main__':
    main()
