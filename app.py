from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *

from config import Channel_Access_Token, Channel_Secret

import beauty_spider
import girl_spider
import cat_spider
import handsome_spider
import Divination
import av_pic_spider
import random_food
import google_search
import get_horoscope
import dice18
import random

app = Flask(__name__)
# Channel Access Token
line_bot_api = LineBotApi(Channel_Access_Token)
# Channel Secret
handler = WebhookHandler(Channel_Secret)


# 監聽所有來自 /callback 的 Post Request
@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'


# 處理訊息
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    keyword = event.message.text
    print("event.message.text:", keyword)

    fate_keyword = "運勢"
    zodiac_keyword = '座'
    if keyword.find(fate_keyword) != -1:
        if keyword.find(zodiac_keyword) != -1:
            today_divination = get_horoscope.main(keyword[:-3])
            if not today_divination:
                return 0
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text=today_divination))
            return 0
        else:
            today_divination = Divination.get_divination()
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text=today_divination))
            return 0

    food_keyword = "吃什麼"
    if keyword.find(food_keyword) != -1:
        today_food = random_food.get_food()
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=today_food))
        return 0

    dice_keyword = "擲骰子"
    if keyword.find(dice_keyword) != -1:
        get_dice_num = dice18.main()
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=get_dice_num))
        return 0

    if keyword == '抽':
        # random_num = random.randint(0, 1)
        # if random_num == 0:
        #     img_url = beauty_spider.main()
        # else:
        #     img_url = girl_spider.main()
        img_url = beauty_spider.main()
        print("App img_url : " + img_url)
        message = ImageSendMessage(
            original_content_url=img_url,
            preview_image_url=img_url
        )
        line_bot_api.reply_message(event.reply_token, message)
        return 0

    if keyword == '抽貓咪':
        img_url = cat_spider.main()
        print("App img_url : " + img_url)
        message = ImageSendMessage(
            original_content_url=img_url,
            preview_image_url=img_url
        )
        line_bot_api.reply_message(event.reply_token, message)
        return 0

    if keyword == '抽帥哥':
        img_url = handsome_spider.main()
        print("App img_url: " + img_url)
        message = ImageSendMessage(
            original_content_url=img_url,
            preview_image_url=img_url
        )
        line_bot_api.reply_message(event.reply_token, message)
        return 0

    if keyword == '紳士的法則':
        img_url = av_pic_spider.main()
        message = ImageSendMessage(
            original_content_url=img_url,
            preview_image_url=img_url
        )
        line_bot_api.reply_message(event.reply_token, message)

        return 0

    google_keyword = "google "
    if keyword.find(google_keyword) != -1:
        search_word = keyword[7:]
        content = google_search.googleSearch(search_word)
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=content))
        return 0

    kerker_keyword = "科科"
    if keyword.find(kerker_keyword) != -1:
        sticker_message = StickerSendMessage(
            package_id='11537',
            sticker_id='52002744'
        )
        line_bot_api.reply_message(
            event.reply_token,
            sticker_message)
        return 0

    if event.message.text == "/help":
        buttons_template = TemplateSendMessage(
            alt_text='Services Template',
            template=ButtonsTemplate(
                title='選擇服務',
                text='請選擇',
                thumbnail_image_url='https://i.imgur.com/pBgoR3W.jpg',
                actions=[
                    MessageTemplateAction(
                        label='等等想吃什麼?',
                        text='等等想吃什麼?'
                    ),
                    MessageTemplateAction(
                        label='表特版妹子',
                        text='抽'
                    ),
                    MessageTemplateAction(
                        label='西斯好圖',
                        text='抽西斯'
                    ),
                    MessageTemplateAction(
                        label='今日運勢',
                        text='今日運勢'
                    )
                ]
            )
        )
        line_bot_api.reply_message(event.reply_token, buttons_template)
        return 0

import os

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
