import requests
from bs4 import BeautifulSoup
from config import tw_horoscope, en_horoscope


def main(keyword):
    # search param
    daily_zodiac = ''
    for idx, zodiac in enumerate(tw_horoscope):
        if keyword.find(zodiac) != -1:
            daily_zodiac = en_horoscope[idx]
            break
        if idx == 11:
            return
    daily_zodiac_url = 'https://www.daily-zodiac.com/mobile/zodiac/' + daily_zodiac
    req = requests.get(daily_zodiac_url)
    # Check status code
    if req.status_code == requests.codes.ok:
        bs_parsing_result = BeautifulSoup(req.text, "html.parser")
        # CSS selector
        selection_title = bs_parsing_result.select('ul.today > li')
        temp_time = str(selection_title[1])[4:]
        selection_result = bs_parsing_result.select('div.text > section > article')
        temp_article = str(selection_result[0])[10:]
        result = temp_time[:-5] + '\n' + daily_zodiac + ' 今日運勢\n' + temp_article[:-19]
        return result
    else:
        print(req.status_code)
        return 0


if __name__ == '__main__':
    main()
