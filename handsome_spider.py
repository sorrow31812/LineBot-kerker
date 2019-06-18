import requests
import random
from bs4 import BeautifulSoup
# from config import Search_list


def main():
    handsome_url = 'https://www.pexels.com/search/handsome'
    req = requests.get(handsome_url)
    # Check status code
    if req.status_code == requests.codes.ok:
        bsParsingResult = BeautifulSoup(req.text, "html.parser")
        # CSS selector
        selectionResult = bsParsingResult.select('div.photos__column')
        article_num = random.randint(0, 2)
        articleResult = selectionResult[article_num].select('div.hide-featured-badge > article')
        img_num = random.randint(0, len(articleResult) - 1)
        url = articleResult[img_num].get('data-photo-modal-image-src')
        return url
    else:
        print(req.status_code)
        return '503 Server'


if __name__ == '__main__':
    main()
