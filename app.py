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

cats_N = ['橘貓', '黑貓', '白貓', '藍貓', '奶油貓', '三花貓', '玳瑁貓', '賓士貓', '乳牛貓', '灰虎斑貓', '棕虎斑貓', '三花虎斑貓', '白底灰虎斑貓', '白底棕虎斑貓', '白底橘虎斑貓', '黑底白襪貓', '橘底白襪貓', '灰底白襪貓', '棕底白襪貓']
cats_R = ['啵啵貓', '尷尬貓', '哭哭貓', '無耳貓', '九命貓', '豹貓', '暹羅貓', '布偶貓', '無毛貓', '波斯貓', '緬因貓', '美國捲耳貓', '挪威森林貓', '狸貓', '熊貓']
cats_SR = ['薄荷冰淇淋貓', '草莓蛋糕貓', '香蕉巧克力貓', '外星幽浮貓', '藍莓優格貓', '柳橙果醬貓', '戀愛棉花糖貓', '宇治抹茶貓', '櫻桃馬卡龍貓', '檸檬汽水貓']
cats_SSR = ['彩虹獨角貓', '白金鑽石貓', '黑夜伯爵貓', '月光精靈貓', '尊絕不凡天使貓', '混沌帝王惡魔貓']
actions = ['叼著魚走了出來，跟你說午安。', '正在偷偷看著你。', '在等你給他吃高級牛肉罐頭。', '正在籌辦一場貓咪演唱會。', '慵懶地在屋頂上睡覺。','與其他貓咪一起打瞌睡。', '正摩擦著你的腿。', '在廚房偷吃魚骨頭。']

def generate_random_cat():
    cat_name = random.choice(cats_N)
    cat_rarity = random.choices([1, 2, 3, 4], weights=[75, 15, 7, 3])[0]
    if cat_rarity == 4:
        cat_name = random.choice(cats_SSR)
    elif cat_rarity == 3:
        cat_name = random.choice(cats_SR)
    elif cat_rarity == 2:
        cat_name = random.choice(cats_R)
    cat_action = random.choice(actions)
    return cat_name, cat_rarity, cat_action

def generate_cat_card(name, rarity, action):
    card = {
        "type": "bubble",
        "header": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                    "type": "text",
                    "text": name,
                    "size": "xl",
                    "weight": "bold",
                    "color": "#FFFFFF"
                }
            ],
            "backgroundColor": "#FF8C00"
        },
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                    "type": "text",
                    "text": "稀有度: " + str(rarity),
                    "color": "#AAAAAA"
                },
                {
                    "type": "text",
                    "text": "動作: " + action,
                    "wrap": True
                }
            ]
        }
    }
    return card

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
    if event.message.text == '抽貓咪':
        cat_name, cat_rarity, cat_action = generate_random_cat()
        card = generate_cat_card(cat_name, cat_rarity, cat_action)
        line_bot_api.reply_message(
            event.reply_token,
            FlexSendMessage(alt_text="發現貓咪！", contents=card)
        )

if __name__ == "__main__":
    app.run()
