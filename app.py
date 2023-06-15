from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import *
import os
import random

app = Flask(__name__)

encountered_cats = []
encountered_species = []

line_bot_api = LineBotApi(os.environ['CHANNEL_ACCESS_TOKEN'])
handler = WebhookHandler(os.environ['CHANNEL_SECRET'])


cats_N = ['橘貓', '黑貓', '白貓', '藍貓', '奶油貓', '三花貓', '玳瑁貓', '賓士貓', '乳牛貓', '灰虎斑貓', '棕虎斑貓', '三花虎斑貓', '白底灰虎斑貓', '白底棕虎斑貓', '白底橘虎斑貓', '黑底白襪貓', '橘底白襪貓', '灰底白襪貓', '棕底白襪貓', '啵啵貓', '尷尬貓', '哭哭貓', '無耳貓', '九命貓', '豹貓', '暹羅貓', '布偶貓', '無毛貓', '波斯貓', '緬因貓', '美國捲耳貓', '挪威森林貓', '狸貓', '熊貓']
cats_R = ['薄荷冰淇淋貓', '草莓蛋糕貓', '香蕉巧克力貓', '外星幽浮貓', '藍莓優格貓', '柳橙果醬貓', '戀愛棉花糖貓', '宇治抹茶貓', '櫻桃馬卡龍貓', '檸檬汽水貓']
cats_SR = ['彩虹獨角貓', '白金鑽石貓', '黑夜伯爵貓', '月光精靈貓']
cats_SSR = ['尊絕不凡天使貓', '混沌帝王惡魔貓']
actions = ['叼著魚走ㄌ出來，跟尼說午安。', '正在偷偷看著尼。', '在等尼給他吃高級牛肉罐頭。', '正在籌辦一場貓咪演唱會。', '把尼的耳機藏起來了，想說尼可以多陪他玩玩。', '正在決定要不要把抓來的老鼠禮物放在尼的床上。', '慵懶ㄉ在屋頂上睡覺覺。','與其他貓咪一起打瞌睡。', '正摩擦著尼ㄉ腿討摸摸。', '玩耍時不小心撞到牆壁，尷尬ㄉ跑開。', '在房間裡找尋一個舒適ㄉ角落休息。', '跟一隻蝴蝶在玩追逐遊戲。', '跳上ㄌ高處觀察窗外ㄉ景色。', '正在學習新ㄉ抓癢技巧。', '悠閒ㄉ舔毛中。', '在花園裡追逐蝴蝶。', '正在曬日光浴。', '躺在窗台上觀察外面ㄉ鳥兒。', '正在玩一隻貓ㄉ捉迷藏。', '正在玩廢紙球。', '正在挖掘地毯下ㄉ秘密。', '正在思考宇宙ㄉ奧秘。', '在玩具老鼠前舞動尾巴。', '正在與貓友進行友誼戰。', '在陽台上耍廢。', '正趴在鋼琴上嘗試彈出一首貓曲。', '悄悄ㄉ爬上ㄌ樹頂想偷窺尼。', '趴在窗戶旁觀察松鼠。', '正在捕捉空氣中ㄉ灰塵。', '正在幫另一隻貓咪洗澡澡。', '在藝術品旁邊擺出ㄌ優雅ㄉ姿勢。', '滾來滾去，像一坨毛球。', '正在學習玩逗貓棒ㄉ技巧。', '在紙箱裡窩著，做白日夢。', '坐在窗戶旁邊與白雲一起午睡。', '正在玩2048。', '正在玩俄羅斯方塊。', '打破ㄌ花瓶。', '打翻ㄌ電腦鍵盤旁邊ㄉ咖啡。','把你ㄉ衛生紙捲咬到地上都是。','跳進ㄌ貓咪隧道裡探險。', '正在訓練自己ㄉ狩獵技巧。', '躺在你ㄉ懷裡踏踏。', '正在玩POPCAT。', '正在搖屁屁。', '趴在暖爐旁邊感受溫暖。', '在房間四處遊蕩，尋找新玩具。', '在電視機前坐著，好奇地看著新聞。', '踩著鋼琴鍵盤，彈奏出一段奇妙ㄉ旋律。', '在沙灘上挖ㄌ好多洞，等待獵物。', '在玩蓮蓬頭，搞得全身溼答答。', '正打算悄悄溜進尼ㄉ枕頭下面。', '在舞池跳舞，展現出驚人ㄉ舞技。', '在思考征服人類的方法。', '開心ㄉ呼嚕呼嚕。', '剛看完一場悲情電影，正在偷哭。', '正在研發時光機。']


def generate_random_cat():
    cat_rarity = random.choices(['N', 'R', 'SR', 'SSR'], weights=[75, 15, 8, 2], k=1)[0]
    if cat_rarity == "N":
        cat_species = random.choice(cats_N)
    elif cat_rarity == "R":
        cat_species = random.choice(cats_R)
    elif cat_rarity == "SR":
        cat_species = random.choice(cats_SR)
    else:
        cat_species = random.choice(cats_SSR)
    if cat_species not in encountered_species:
        encountered_species.append(cat_species)
    encountered_cats.append(cat_species)
    
    return cat_species, cat_rarity, random.choice(actions)


def generate_cat_card(name, rarity, action):
    color = "#7EAEF6"  # 預設顏色為 N 稀有度的顏色
    if rarity == "N":
        color = "#7CC400"
    elif rarity == "R":
        color = "#90ABDD"
    elif rarity == "SR":
        color = "#F1D91D"
    elif rarity == "SSR":
        color = "#C696BE"
        
    cat_images = {
        "橘貓": "https://i.imgur.com/RxU0fNb.jpg",
        "黑貓": "https://i.imgur.com/gmQN2Na.jpg",
        "白貓": "https://i.imgur.com/Jfqak5C.jpg",
        "藍貓": "https://i.imgur.com/eFuVG7W.jpg",
        "奶油貓": "https://i.imgur.com/Z14nDTD.jpg",
        "三花貓": "https://i.imgur.com/dWKXjci.jpg",
        "玳瑁貓": "https://i.imgur.com/1M1UhDb.jpg",
        "賓士貓": "https://i.imgur.com/cXy7Tc7.jpg",
        "乳牛貓": "https://i.imgur.com/Xi2XL5j.jpg",
        "灰虎斑貓": "https://i.imgur.com/YDASMm9.jpg",
        "棕虎斑貓": "https://i.imgur.com/kK6hLoq.jpg",
        "三花虎斑貓": "https://i.imgur.com/Z2v9zhG.jpg",
        "白底灰虎斑貓": "https://i.imgur.com/z4dBGP4.jpg",
        "白底棕虎斑貓": "https://i.imgur.com/5Vc3Wey.jpg",
        "白底橘虎斑貓": "https://i.imgur.com/7mcVdUC.jpg",
        "黑底白襪貓": "https://i.imgur.com/NIMGa0C.jpg",
        "橘底白襪貓": "https://i.imgur.com/MZhr3Fg.jpg",
        "灰底白襪貓": "https://i.imgur.com/h6Qcrzv.jpg",
        "棕底白襪貓": "https://i.imgur.com/Q6NC4rd.jpg",
        "啵啵貓": "https://i.imgur.com/h89bb9g.jpg",
        "尷尬貓": "https://i.imgur.com/xQZuNX5.jpg",
        "哭哭貓": "https://i.imgur.com/TZHMKTA.jpg",
        "無耳貓": "https://i.imgur.com/vIILgxw.jpg",
        "九命貓": "https://i.imgur.com/kfakUvR.jpg",
        "豹貓": "https://i.imgur.com/8IYkuXJ.jpg",
        "暹羅貓": "https://i.imgur.com/zu3ZhlS.jpg",
        "布偶貓": "https://i.imgur.com/wlyxgbx.jpg",
        "無毛貓": "https://i.imgur.com/xLldBNq.jpg",
        "波斯貓": "https://i.imgur.com/e6TOW5O.jpg",
        "緬因貓": "https://i.imgur.com/WJfMq19.jpg",
        "美國捲耳貓": "https://i.imgur.com/x3DzRA1.jpg",
        "挪威森林貓": "https://i.imgur.com/s1Fsm5U.jpg",
        "狸貓": "https://i.imgur.com/K7SHhoO.jpg",
        "熊貓": "https://i.imgur.com/fgtYCCS.jpg",
        "薄荷冰淇淋貓": "https://i.imgur.com/BCRXZeL.jpg",
        "草莓蛋糕貓": "https://i.imgur.com/o4nmshr.jpg",
        "香蕉巧克力貓": "https://i.imgur.com/4yzcm0z.jpg",
        "外星幽浮貓": "https://i.imgur.com/LH4MtLL.jpg",
        "藍莓優格貓": "https://i.imgur.com/YsBVeE3.jpg",
        "柳橙果醬貓": "https://i.imgur.com/fN6MZDO.jpg",
        "戀愛棉花糖貓": "https://i.imgur.com/0ru502I.jpg",
        "宇治抹茶貓": "https://i.imgur.com/zJiJjpy.jpg",
        "櫻桃馬卡龍貓": "https://i.imgur.com/5btCBHu.jpg",
        "檸檬汽水貓": "https://i.imgur.com/kGjVBV5.jpg",

    }
    
    
    if name in cat_images:
        image_url = cat_images[name]
    else:
        image_url = "https://i.imgur.com/3ky4O6P.jpg"  # 如果找不到對應的貓咪圖片，則使用預設圖片的 URL


    card = {
        "type": "bubble",
        "header": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                    "type": "text",
                    "text": name + " 出現了！",
                    "size": "lg",
                    "weight": "bold",
                    "color": "#FFFFFF",
                    "align": "center"
                }
            ],
            "backgroundColor": color  # 使用根據稀有度設定的顏色
        },
        "hero": {
            "type": "image",
            "url": image_url,
            "size": "full"
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
                    "text": action,
                    "wrap": True
                }
            ],
        },
        "footer": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                    "type": "button",
                    "action": {
                        "type": "message",
                        "label": "再找一隻貓咪",
                        "text": "找貓咪"
                    },
                    "color": color  # 使用根據稀有度設定的顏色
                },
                {
                    "type": "button",
                    "action": {
                        "type": "message",
                        "label": "數數看窩總共遇見ㄌ幾隻貓咪",
                        "text": "窩遇見ㄌ幾隻貓咪？"
                    },
                    "color": color  # 使用根據稀有度設定的顏色
                },
                {
                    "type": "button",
                    "action": {
                        "type": "message",
                        "label": "數數看窩總共遇見ㄌ幾種貓咪",
                        "text": "窩遇見ㄌ幾種貓咪？"
                    },
                    "color": color  # 使用根據稀有度設定的顏色
                }
            ]
        }
    }
    return card

@app.route('/')
def index():
    return 'Hello World!'

@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

@handler.add(MessageEvent, message=TextMessage)

def handle_message(event):
    global encountered_cats
    global encountered_species
    
    if event.message.text == '找貓咪':
        cat_name, cat_rarity, cat_action = generate_random_cat()
        cat_card = generate_cat_card(cat_name, cat_rarity, cat_action)

        message = FlexSendMessage(alt_text="發現貓咪！", contents=cat_card)
        line_bot_api.reply_message(event.reply_token, message)

    elif event.message.text == "窩遇見ㄌ幾隻貓咪？":
        total_cats = len(encountered_cats)
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=f"尼總共遇見了 {total_cats} 隻貓咪！貓咪永遠不嫌多。"))

    elif event.message.text == "窩遇見ㄌ幾種貓咪？":
        total_species = len(encountered_species)
        if total_species == 50:
            message = "太棒了，尼已經找到ㄌ所有ㄉ貓咪！"
        else:
            waiting_species = 50 - total_species
            message = f"尼總共遇見了 {total_species} 種貓咪！還有 {waiting_species} 種貓咪正在等著尼！"
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=message))

    else:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text="QQ...SORRY，人類有點害羞，不敢跟陌生人聊天，請試著跟貓咪們一起玩8！"))

if __name__ == "__main__":
    app.run()
