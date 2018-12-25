from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *

import beauty_spider

app = Flask(__name__)

# Channel Access Token
line_bot_api = LineBotApi('n3/oHFHwqZ2mQV7pUChishywh66Z9Z0F4uyxtNKj+RK3l4HPBPTgElS19HCK2yrmZW4CLPoyG8yzppQijdpQZ6xLd7Jm9QdOPoTkjRANyB7sB56Zq05UQt4cbmRAEQp1y3B3YBQwHczl/KdotYez8AdB04t89/1O/w1cDnyilFU=')
# Channel Secret
handler = WebhookHandler('ef2da7c9e8a366e6d2ade3eb64fcb8f9')

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
    #message = TextSendMessage(text=event.message.text)
	#message = ImageSendMessage( original_content_url='https://i.imgur.com/xZFUVex.jpg', preview_image_url='https://i.imgur.com/yL7naJ7.jpg' )
    beauty_spider.main(event.message.text)
    message = ImageSendMessage(
        original_content_url='https://i.imgur.com/xZFUVex.jpg',
        preview_image_url='https://i.imgur.com/xZFUVex.jpg'
    )
    line_bot_api.reply_message(event.reply_token, message)

import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
