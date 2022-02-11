from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler 
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

app = Flask(__name__)

#YOUR_CHANNEL_ACCESS_TOKEN
line_bot_api = LineBotApi('Pm4aGfmytf89KFtvfOgt6k+TLIS+KxBlUwD4mFil55cSddwjGvYkAWIYKe9uEb/Rs+d3EMaZ28F1ynVEBrmtcky459/fKjAXwFJTRERzWhn256uAzyWOS1Upn2w+wcZJ9FhiRkgKc3CJW5vHydslIwdB04t89/1O/w1cDnyilFU=')

# channel secret
handler = WebhookHandler('51c326c28e06078b4122a701182dc06f')


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
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    message = TextSendMessage(text=event.message.text)
    line_bot_api.reply_message(event.reply_token, message)

import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)

