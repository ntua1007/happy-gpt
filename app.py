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
actions = ['叼著魚走了出來，跟你說午安。', '正在偷偷看著你。', '在等你給他吃高級牛肉罐頭。', '正在籌辦一場貓咪演唱會。', '慵懶地在屋頂上睡覺。','與其他貓咪一起打瞌睡。', '正摩擦著你的腿討摸摸。', '玩耍時不小心撞到牆壁，尷尬地跑開。', '在房間裡找尋一個舒適的角落休息。', '跟一隻蝴蝶玩追逐遊戲。', '跳上高處觀察窗外的景色。', '正在學習新的抓癢技巧。', '輕輕地舔嘴巴清潔毛髮。', '在花園裡追逐蝴蝶。', '正在曬日光浴。', '躺在窗台上觀察外面的鳥兒。', '正在跳躍著玩捉迷藏。', '正在玩廢紙球。', '正在挖掘地毯下的秘密。', '正在思考宇宙的奧秘。', '在玩具老鼠前舞動尾巴。', '正在與貓友進行友誼戰。', '在陽台上耍廢。', '正在趴在鋼琴上嘗試彈出一首貓曲。', '悄悄地爬上樹頂。', '趴在窗戶旁觀察松鼠。', '正在捕捉空氣中的灰塵。', '正在幫另一隻貓咪洗澡。', '在藝術品旁邊擺出優雅的姿勢。', '滾來滾去，顆一隻毛球。', '正在學習玩逗貓棒的技巧。', '在紙箱裡窩著，做白日夢。', '坐在窗戶旁邊與白雲一起午睡。', '正在玩2048。', '正在玩俄羅斯方塊。', '打破了花瓶。', '跳進了貓咪隧道裡探險。', '正在訓練自己的狩獵技巧。', '躺在你的懷裡踏踏。', '正在玩POPCAT。', '正在搖屁屁。', '趴在暖爐旁邊感受溫暖。', '在房間四處遊蕩，尋找新玩具。', '在電視機前坐著，好奇地看著新聞。', '踩著鋼琴鍵盤，彈奏出一段奇妙的旋律。', '在沙灘上挖洞，冒出貓頭嚇人。', '在玩蓮蓬頭，搞得全身溼答答。', '正打算悄悄溜進你的枕頭下面。', '在牆上跳舞，展現出驚人的舞技。']

def generate_random_cat():
    rarity = random.choices(['N', 'R', 'SR', 'SSR'], weights=[68, 20, 8, 4])[0]
    if rarity == 'N':
        cat = random.choice(cats_N)
    elif rarity == 'R':
        cat = random.choice(cats_R)
    elif rarity == 'SR':
        cat = random.choice(cats_SR)
    else:
        cat = random.choice(cats_SSR)
    
    action = random.choice(actions)
    
    return f'{cat} {action}'


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
    
    if msg  == "找貓咪2":
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=generate_random_cat()))
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



    # random_cat = generate_random_cat()
    # print(random_cat)
    # reply_msg = get_random_cat()
    # line_bot_api.reply_message(event.reply_token, TextSendMessage(text=reply_msg))

   
import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
