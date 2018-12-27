from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *

import configparser

import beauty_spider
import Divination

app = Flask(__name__)
config = configparser.ConfigParser()
config.read("config.ini")
# Channel Access Token
line_bot_api = LineBotApi(config['line_bot']['Channel_Access_Token'])
# Channel Secret
handler = WebhookHandler(config['line_bot']['Channel_Secret'])


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
    print("event.reply_token:", event.reply_token)
    print("event.message.text:", keyword)
    # if event.message.image:
    #     print("Image exist")
    #     return 0
    if keyword == '抽':
        img_url = beauty_spider.main()
        print("App img_url : " + img_url)
        message = ImageSendMessage(
            original_content_url=img_url,
            preview_image_url=img_url
        )
        line_bot_api.reply_message(event.reply_token, message)
        return 0
    fate_keyword = "運勢"
    if keyword.find(fate_keyword) != -1:
        today_divination = Divination.get_divination()
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=today_divination))
    # TBD
    # google search, ptt sex, upload image


import os

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
