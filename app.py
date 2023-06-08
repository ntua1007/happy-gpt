from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import *
import os
import random
import openai

app = Flask(__name__)

line_bot_api = LineBotApi(os.environ['CHANNEL_ACCESS_TOKEN'])
handler = WebhookHandler(os.environ['CHANNEL_SECRET'])
openai.api_key = os.environ['OPENAI_SECRET']


@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    card = {
              "type": "bubble",
              "hero": {
                "type": "image",
                "url": "https://lions-clubs.dev2.rib.tw/static/documents/images/Lions_Clubs_International.png",
                "size": "full",
                "aspectRatio": "1:1",
                "aspectMode": "cover",
                "action": {
                  "type": "uri",
                  "uri": "http://linecorp.com/"
                }
              },
              "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                  {
                    "type": "text",
                    "text": "113年度獲獎獅友名單",
                    "weight": "bold",
                    "size": "xl"
                  }
                ]
              },
              "footer": {
                "type": "box",
                "layout": "vertical",
                "spacing": "sm",
                "contents": [
                  {
                    "type": "button",
                    "style": "link",
                    "height": "sm",
                    "action": {
                      "type": "uri",
                      "label": "公文連結",
                      "uri": "https://lions-clubs.dev2.rib.tw"
                    }
                  }
                ],
                "flex": 0
              }
            }

    msg = event.message.text
    if msg  == "找貓咪":
        line_bot_api.reply_message(
            event.reply_token,
            FlexSendMessage(alt_text="發現貓咪！", contents=card))
        return
    ai_msg = msg[:6].lower()
    if ai_msg == 'hi ai:':
            # 將第六個字元之後的訊息發送給 OpenAI
            response = openai.Completion.create(
                model='text-davinci-003',
                prompt=msg[6:],
                max_tokens=256,
                temperature=0.5,
                )
            # 接收到回覆訊息後，移除換行符號
            reply_msg = TextSendMessage(text=response["choices"][0]["text"].replace('\n',''))

            
    import random

    cats_common = ['橘貓', '黑貓', '白貓', '藍貓', '奶油貓', '三花貓', '玳瑁貓', '賓士貓', '乳牛貓', '灰虎斑貓', '棕虎斑貓', '三花虎斑貓', '白底灰虎斑貓', '白底棕虎斑貓', '白底橘虎斑貓', '黑底白襪貓', '橘底白襪貓', '灰底白襪貓', '棕底白襪貓']
    cats_rare = ['啵啵貓', '尷尬貓', '哭哭貓', '無耳貓', '九命貓', '豹貓', '暹羅貓', '布偶貓', '無毛貓', '波斯貓', '緬因貓', '美國捲耳貓', '挪威森林貓', '狸貓', '熊貓']
    cats_epic = ['薄荷冰淇淋貓', '草莓蛋糕貓', '香蕉巧克力貓', '外星幽浮貓', '藍莓優格貓', '柳橙果醬貓', '戀愛棉花糖貓', '宇治抹茶貓', '櫻桃馬卡龍貓', '檸檬汽水貓']
    cats_legendary = ['彩虹獨角貓', '白金鑽石貓', '黑夜伯爵貓', '月光精靈貓', '尊絕不凡天使貓', '混沌帝王惡魔貓']

    rarity_weights = [0.68, 0.20, 0.08, 0.04]

    def get_random_cat():
    rarity = random.choices(['common', 'rare', 'epic', 'legendary'], weights=rarity_weights)[0]
    if rarity == 'common':
        return random.choice(cats_common)
    elif rarity == 'rare':
        return random.choice(cats_rare)
    elif rarity == 'epic':
        return random.choice(cats_epic)
    elif rarity == 'legendary':
        return random.choice(cats_legendary)

    reply_msg = get_random_cat()
    line_bot_api.reply_message(event.reply_token, TextSendMessage(text=reply_msg))

   
import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
