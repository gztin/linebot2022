from webbrowser import get
from linebot.models import MessageEvent, TextMessage, TextSendMessage, ImageSendMessage, StickerSendMessage, LocationSendMessage, QuickReply, QuickReplyButton, MessageAction
from linebot.models import MessageEvent, TextMessage, PostbackEvent, TextSendMessage, TemplateSendMessage, ConfirmTemplate, MessageTemplateAction, ButtonsTemplate, PostbackTemplateAction, URITemplateAction, CarouselTemplate, CarouselColumn, ImageCarouselTemplate, ImageCarouselColumn
from linebot.exceptions import InvalidSignatureError
from linebot import LineBotApi, WebhookHandler
from flask import request, abort
from flask import Flask
import requests
from bs4 import BeautifulSoup
import random

app = Flask(__name__)

line_bot_api = LineBotApi(
    'W4rZuPsIe7y1kPsOV+1d+oidB9R7uDuLlGxYELp1ScAOZXFihE7aAVOE9oSc8B0H14el+d/L+ev1Qv9GS8UhAZ06qcNvG/07FVMZ91AAiazxQnBdFpG5rd9nJ62knD2lI/Fs5NmSIAVNBk52rIt0hQdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('c90ce7e0b40bea4fd79c5ddda2621a46')


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
    mtext = event.message.text
    if mtext == '寶早安':
        sendCarousel(event)

    elif mtext == '@看八卦版':
        try:
            content = []
            url = f"https://opensheet.elk.sh/1oHKxASVeO6EpHlBE0Um9sQBoIDErAoJIItUGelSFMaE/grosspingData"
            headers = {
                "user-agent": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36"
            }
            r = requests.get(url)
            data =  r.json()
            for i in data[0:10]:
                title = i.get("mtitle")
                link = i.get("mlink")
                content += [title + link]

            line_bot_api.reply_message(
                event.reply_token, TextSendMessage(text='\n\n'.join(content)))
        except:
            line_bot_api.reply_message(
                event.reply_token, TextSendMessage(text='發生錯誤！'))

    elif mtext == '@如何查詢空氣品質':
        try:
            content = '參考輸入範例:'+'\n\n''"台北空氣"'+'\n'+'"萬華區空氣品質"'+'\n'+'"台中aqi"'
            
            line_bot_api.reply_message(
                event.reply_token, TextSendMessage(text=content))
        except:
            line_bot_api.reply_message(
                event.reply_token, TextSendMessage(text='發生錯誤！'))

    elif mtext == '@看表特版':
        try:
            content = []
            url = f"https://opensheet.elk.sh/1dOCnHtNRSo4X1SA02NcubK62QINsJ5GM8T6ApLJAf00/beautyArticle"
            r = requests.get(url)
            data =  r.json()
            for i in data[0:10]:
                title = i.get("mtitle")
                link = i.get("mlink")
                content += [title + link]

            line_bot_api.reply_message(
                event.reply_token, TextSendMessage(text='\n\n'.join(content)))
        except:
            line_bot_api.reply_message(
                event.reply_token, TextSendMessage(text='發生錯誤！'))

    elif mtext == '@看熱門新聞':
        try:
            content = []

            url = 'https://news.ltn.com.tw/list/breakingnews/popular'
            web = requests.get(url)
            soup = BeautifulSoup(web.text, "html.parser")
            news = soup.select('div.whitecon > ul > li')
            for i in news[0:10]:
                title = i.find('a')['title']
                link = i.find('a')['href']
                content += [title + link]
            line_bot_api.reply_message(
                event.reply_token, TextSendMessage(text='\n\n'.join(content)))
        except:
            line_bot_api.reply_message(
                event.reply_token, TextSendMessage(text='發生錯誤！'))

    elif mtext == '@批踢踢熱門文章':
        try:
            content = []
            url = f"https://opensheet.elk.sh/1ulYVMWJqOWLIeBlYDzfR6LtOxmErrxPPuoJZGJQoOP0/articleHot"
            r = requests.get(url)
            data =  r.json()
            for i in data[0:10]:
                title = i.get("mtitle")
                link = i.get("mlink")
                content += [title + link]

            line_bot_api.reply_message(
                event.reply_token, TextSendMessage(text='\n\n'.join(content)))
        except:
            line_bot_api.reply_message(
                event.reply_token, TextSendMessage(text='發生錯誤！'))

    elif mtext == '@傳送文字':
        try:
            message = TextSendMessage(
                text="我是 Linebot，\n您好！"
            )
            line_bot_api.reply_message(event.reply_token, message)
        except:
            line_bot_api.reply_message(
                event.reply_token, TextSendMessage(text='發生錯誤！'))

    elif mtext == '@看今日運勢':
        try:
            # fate = ['凶', '大凶', '平', '末吉', '小吉', '中吉', '大吉', ]
            # result = random.choice(fate)
            result = random.choice(range(1, 100))
            resultNumber = result
            fateNumber = str(resultNumber)
            poemNumber = "抽到籤號:"+fateNumber

            urlBook = f"https://opensheet.elk.sh/1-iH-YGEgyEkjrV2bM_sWR2MytqcfJf0ySiCugaiAgJw/fateData"
            headers = {
                "user-agent": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36"
            }
            r_book = requests.get(urlBook, headers=headers)
            data_store = r_book.json()
            poem = data_store[result]

            r1 = poem["poemType"]
            r2 = poem["poemContent"]
            r3 = poem["poemNote"]

            line_bot_api.reply_message(
                event.reply_token, TextSendMessage(text=poemNumber+'\n\n'+r1+'\n\n'+r2+'\n\n'+r3))
        except:
            line_bot_api.reply_message(
                event.reply_token, TextSendMessage(text='發生錯誤！'))

    elif mtext == '@最近熱門電影':
        try:
            content = []
            url = f"https://opensheet.elk.sh/1F9o9xlCVKXEkxcHGKR1gPUsxArhdheQ_Hf0f3MFAohw/movieList"
            headers = {
                "user-agent": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36"
            }
            r = requests.get(url)
            data =  r.json()
            for i in data[0:9]:
                title = i.get("movieName")
                link = i.get("movieInfLink")
                content += [title + link]

            line_bot_api.reply_message(
                event.reply_token, TextSendMessage(text='\n\n'.join(content)))
        except:
            line_bot_api.reply_message(
                event.reply_token, TextSendMessage(text='發生錯誤！'))

    elif '區空氣品質' in mtext:
        try:
            
            content = []
            # 取得要查詢的區域
            typeWords = mtext.split('區')[0]
            
            url = f'https://opensheet.elk.sh/1pqyY2HRSqINHC35lcm04POR-MeQZTU835DGktbET-HU/testData'
            r = requests.get(url)
            data = r.json()
            
            for i in data:
                if typeWords == i.get("sitename"):
                    site = i.get("sitename");
                    aqi = i.get("aqi");
                    pm = i.get("pm2.5");
                
            line_bot_api.reply_message(
                event.reply_token, TextSendMessage(
                    text='您查詢的資料如下:'+
                        '\n\n'+'監測站:'+site+
                        '\n'+'aqi 空氣指標:'+aqi+
                        '\n'+'PM2.5 :'+pm))
        except:
            line_bot_api.reply_message(
                event.reply_token, TextSendMessage(text='發生錯誤！'))
    
    elif '空氣' in mtext:
        try:
            
            content = []
            # 取得要查詢的區域，如果輸入桃園aqi
            typeWords = mtext.split('空氣')[0]
            
            url = f'https://opensheet.elk.sh/1pqyY2HRSqINHC35lcm04POR-MeQZTU835DGktbET-HU/testData'
            r = requests.get(url)
            data = r.json()
            
            if '台北'in typeWords:
                typeWords = typeWords.replace('台北','臺北市')
            
                for i in data:
                    if typeWords == i.get("county"):
                        site = i.get("sitename");
                        aqi = i.get("aqi");
                        content += [site+'站的aqi值為:'+aqi]
            
            elif ('全臺'in typeWords)|('全台'in typeWords):
                for i in data:
                    site = i.get("sitename");
                    aqi = i.get("aqi");
                    content += [site+'站的aqi值為:'+aqi]
                        
            elif '臺北'in typeWords:
                typeWords = typeWords.replace('臺北','臺北市')
                for i in data:
                    if typeWords == i.get("county"):
                        site = i.get("sitename");
                        aqi = i.get("aqi");
                        content += [site+'站的aqi值為:'+aqi]
            
            elif '台中'in typeWords:
                typeWords = typeWords.replace('台中','臺中市')
                for i in data:
                    if typeWords == i.get("county"):
                        site = i.get("sitename");
                        aqi = i.get("aqi");
                        content += [site+'站的aqi值為:'+aqi]
            
            elif '臺中'in typeWords:
                typeWords = typeWords.replace('臺中','臺中市')
                for i in data:
                    if typeWords == i.get("county"):
                        site = i.get("sitename");
                        aqi = i.get("aqi");
                        content += [site+'站的aqi值為:'+aqi]
            
            elif '苗栗'in typeWords:
                typeWords = typeWords.replace('苗栗','苗栗縣')
                for i in data:
                    if typeWords == i.get("county"):
                        site = i.get("sitename");
                        aqi = i.get("aqi");
                        content += [site+'站的aqi值為:'+aqi]
            
            elif '彰化'in typeWords:
                typeWords = typeWords.replace('彰化','彰化縣')
                for i in data:
                    if typeWords == i.get("county"):
                        site = i.get("sitename");
                        aqi = i.get("aqi");
                        content += [site+'站的aqi值為:'+aqi]
            
            elif '南投'in typeWords:
                typeWords = typeWords.replace('南投','南投縣')
                for i in data:
                    if typeWords == i.get("county"):
                        site = i.get("sitename");
                        aqi = i.get("aqi");
                        content += [site+'站的aqi值為:'+aqi]
            
            elif '雲林'in typeWords:
                typeWords = typeWords.replace('雲林','雲林縣')
                for i in data:
                    if typeWords == i.get("county"):
                        site = i.get("sitename");
                        aqi = i.get("aqi");
                        content += [site+'站的aqi值為:'+aqi]
            
            elif '屏東'in typeWords:
                typeWords = typeWords.replace('屏東','屏東市')
                for i in data:
                    if typeWords == i.get("county"):
                        site = i.get("sitename");
                        aqi = i.get("aqi");
                        content += [site+'站的aqi值為:'+aqi]
            
            elif '宜蘭'in typeWords:
                typeWords = typeWords.replace('宜蘭','宜蘭縣')
                for i in data:
                    if typeWords == i.get("county"):
                        site = i.get("sitename");
                        aqi = i.get("aqi");
                        content += [site+'站的aqi值為:'+aqi]
            
            elif '金門'in typeWords:
                typeWords = typeWords.replace('金門','金門縣')
                for i in data:
                    if typeWords == i.get("county"):
                        site = i.get("sitename");
                        aqi = i.get("aqi");
                        content += [site+'站的aqi值為:'+aqi]
            
            elif '台南'in typeWords:
                typeWords = typeWords.replace('台南','臺南市')
                for i in data:
                    if typeWords == i.get("county"):
                        site = i.get("sitename");
                        aqi = i.get("aqi");
                        content += [site+'站的aqi值為:'+aqi]
            
            elif '臺南'in typeWords:
                typeWords = typeWords.replace('臺南','臺南市')
                for i in data:
                    if typeWords == i.get("county"):
                        site = i.get("sitename");
                        aqi = i.get("aqi");
                        content += [site+'站的aqi值為:'+aqi]
           
            elif '桃園'in typeWords:
                typeWords = typeWords.replace('桃園','桃園市')
                for i in data:
                    if typeWords == i.get("county"):
                        site = i.get("sitename");
                        aqi = i.get("aqi");
                        content += [site+'站的aqi值為:'+aqi]
            
            elif '基隆'in typeWords:
                typeWords = typeWords.replace('基隆','基隆市')
                for i in data:
                    if typeWords == i.get("county"):
                        site = i.get("sitename");
                        aqi = i.get("aqi");
                        content += [site+'站的aqi值為:'+aqi]
            
            elif '高雄'in typeWords:
                typeWords = typeWords.replace('高雄','高雄市')
                for i in data:
                    if typeWords == i.get("county"):
                        site = i.get("sitename");
                        aqi = i.get("aqi");
                        content += [site+'站的aqi值為:'+aqi]
                
            elif '新竹'in typeWords:
                typeWords = typeWords.replace('新竹','新竹市')
                typeWords2 = typeWords.replace('新竹市','新竹縣')
                for i in data:
                    if typeWords == i.get("county"):
                        site = i.get("sitename");
                        aqi = i.get("aqi");
                        content += [site+'站的aqi值為:'+aqi]
                
                for i in data:
                    if typeWords2 == i.get("county"):
                        site = i.get("sitename");
                        aqi = i.get("aqi");
                        content += [site+'站的aqi值為:'+aqi]
                
            elif '嘉義'in typeWords:
                typeWords = typeWords.replace('嘉義','嘉義市')
                typeWords2 = typeWords.replace('嘉義市','嘉義縣')
                for i in data:
                    if typeWords == i.get("county"):
                        site = i.get("sitename");
                        aqi = i.get("aqi");
                        content += [site+'站的aqi值為:'+aqi]
                
                for i in data:
                    if typeWords2 == i.get("county"):
                        site = i.get("sitename");
                        aqi = i.get("aqi");
                        content += [site+'站的aqi值為:'+aqi]
            
            line_bot_api.reply_message(
                event.reply_token, TextSendMessage(
                    text='\n\n'.join(content)))
        except:
            line_bot_api.reply_message(
                event.reply_token, TextSendMessage(text='發生錯誤！'))
    
            
    elif 'aqi' in mtext:
        try:
            
            content = []
            cityList = [
                '臺北市','新北市','基隆市',
                '桃園市','新竹市','新竹縣',
                '苗栗縣','臺中市','彰化縣',
                '南投縣','雲林縣','嘉義縣',
                '台南市','高雄市','屏東縣',
                '宜蘭縣','金門縣','嘉義市']
            
            # 取得要查詢的區域，如果輸入桃園aqi
            typeWords = mtext.split('aq')[0]
            
            url = f'https://opensheet.elk.sh/1pqyY2HRSqINHC35lcm04POR-MeQZTU835DGktbET-HU/testData'
            r = requests.get(url)
            data = r.json()
            
            if '台北'in typeWords:
                typeWords = typeWords.replace('台北','臺北市')
            
                for i in data:
                    if typeWords == i.get("county"):
                        site = i.get("sitename");
                        aqi = i.get("aqi");
                        content += [site+'站的aqi值為:'+aqi]
            
            elif ('全臺'in typeWords)|('全台'in typeWords):
                for i in data:
                    site = i.get("sitename");
                    aqi = i.get("aqi");
                    content += [site+'站的aqi值為:'+aqi]
                        
            elif '臺北'in typeWords:
                typeWords = typeWords.replace('臺北','臺北市')
                for i in data:
                    if typeWords == i.get("county"):
                        site = i.get("sitename");
                        aqi = i.get("aqi");
                        content += [site+'站的aqi值為:'+aqi]
            
            elif '台中'in typeWords:
                typeWords = typeWords.replace('台中','臺中市')
                for i in data:
                    if typeWords == i.get("county"):
                        site = i.get("sitename");
                        aqi = i.get("aqi");
                        content += [site+'站的aqi值為:'+aqi]
            
            elif '臺中'in typeWords:
                typeWords = typeWords.replace('臺中','臺中市')
                for i in data:
                    if typeWords == i.get("county"):
                        site = i.get("sitename");
                        aqi = i.get("aqi");
                        content += [site+'站的aqi值為:'+aqi]
            
            elif '苗栗'in typeWords:
                typeWords = typeWords.replace('苗栗','苗栗縣')
                for i in data:
                    if typeWords == i.get("county"):
                        site = i.get("sitename");
                        aqi = i.get("aqi");
                        content += [site+'站的aqi值為:'+aqi]
            
            elif '彰化'in typeWords:
                typeWords = typeWords.replace('彰化','彰化縣')
                for i in data:
                    if typeWords == i.get("county"):
                        site = i.get("sitename");
                        aqi = i.get("aqi");
                        content += [site+'站的aqi值為:'+aqi]
            
            elif '南投'in typeWords:
                typeWords = typeWords.replace('南投','南投縣')
                for i in data:
                    if typeWords == i.get("county"):
                        site = i.get("sitename");
                        aqi = i.get("aqi");
                        content += [site+'站的aqi值為:'+aqi]
            
            elif '雲林'in typeWords:
                typeWords = typeWords.replace('雲林','雲林縣')
                for i in data:
                    if typeWords == i.get("county"):
                        site = i.get("sitename");
                        aqi = i.get("aqi");
                        content += [site+'站的aqi值為:'+aqi]
            
            elif '屏東'in typeWords:
                typeWords = typeWords.replace('屏東','屏東市')
                for i in data:
                    if typeWords == i.get("county"):
                        site = i.get("sitename");
                        aqi = i.get("aqi");
                        content += [site+'站的aqi值為:'+aqi]
            
            elif '宜蘭'in typeWords:
                typeWords = typeWords.replace('宜蘭','宜蘭縣')
                for i in data:
                    if typeWords == i.get("county"):
                        site = i.get("sitename");
                        aqi = i.get("aqi");
                        content += [site+'站的aqi值為:'+aqi]
            
            elif '金門'in typeWords:
                typeWords = typeWords.replace('金門','金門縣')
                for i in data:
                    if typeWords == i.get("county"):
                        site = i.get("sitename");
                        aqi = i.get("aqi");
                        content += [site+'站的aqi值為:'+aqi]
            
            elif '台南'in typeWords:
                typeWords = typeWords.replace('台南','臺南市')
                for i in data:
                    if typeWords == i.get("county"):
                        site = i.get("sitename");
                        aqi = i.get("aqi");
                        content += [site+'站的aqi值為:'+aqi]
            
            elif '臺南'in typeWords:
                typeWords = typeWords.replace('臺南','臺南市')
                for i in data:
                    if typeWords == i.get("county"):
                        site = i.get("sitename");
                        aqi = i.get("aqi");
                        content += [site+'站的aqi值為:'+aqi]
           
            elif '桃園'in typeWords:
                typeWords = typeWords.replace('桃園','桃園市')
                for i in data:
                    if typeWords == i.get("county"):
                        site = i.get("sitename");
                        aqi = i.get("aqi");
                        content += [site+'站的aqi值為:'+aqi]
            
            elif '基隆'in typeWords:
                typeWords = typeWords.replace('基隆','基隆市')
                for i in data:
                    if typeWords == i.get("county"):
                        site = i.get("sitename");
                        aqi = i.get("aqi");
                        content += [site+'站的aqi值為:'+aqi]
            
            elif '高雄'in typeWords:
                typeWords = typeWords.replace('高雄','高雄市')
                for i in data:
                    if typeWords == i.get("county"):
                        site = i.get("sitename");
                        aqi = i.get("aqi");
                        content += [site+'站的aqi值為:'+aqi]
                
            elif '新竹'in typeWords:
                typeWords = typeWords.replace('新竹','新竹市')
                typeWords2 = typeWords.replace('新竹市','新竹縣')
                for i in data:
                    if typeWords == i.get("county"):
                        site = i.get("sitename");
                        aqi = i.get("aqi");
                        content += [site+'站的aqi值為:'+aqi]
                
                for i in data:
                    if typeWords2 == i.get("county"):
                        site = i.get("sitename");
                        aqi = i.get("aqi");
                        content += [site+'站的aqi值為:'+aqi]
                
            elif '嘉義'in typeWords:
                typeWords = typeWords.replace('嘉義','嘉義市')
                typeWords2 = typeWords.replace('嘉義市','嘉義縣')
                for i in data:
                    if typeWords == i.get("county"):
                        site = i.get("sitename");
                        aqi = i.get("aqi");
                        content += [site+'站的aqi值為:'+aqi]
                
                for i in data:
                    if typeWords2 == i.get("county"):
                        site = i.get("sitename");
                        aqi = i.get("aqi");
                        content += [site+'站的aqi值為:'+aqi]
            
            line_bot_api.reply_message(
                event.reply_token, TextSendMessage(
                    text='\n\n'.join(content)))
        except:
            line_bot_api.reply_message(
                event.reply_token, TextSendMessage(text='發生錯誤！'))
            

    elif mtext == '@傳送圖片':
        try:
            # 接受 1MB 以下的 JPG 圖檔，網址必須是 https 開頭
            message = ImageSendMessage(
                original_content_url="https://i.imgur.com/4QfKuz1.png",
                preview_image_url="https://i.imgur.com/4QfKuz1.png"
            )
            line_bot_api.reply_message(event.reply_token, message)
        except:
            line_bot_api.reply_message(
                event.reply_token, TextSendMessage(text='發生錯誤！'))

    elif mtext == '@傳送貼圖':
        try:
            message = StickerSendMessage(  # 貼圖兩個id需查表
                package_id='1',
                sticker_id='2'
            )
            line_bot_api.reply_message(event.reply_token, message)
        except:
            line_bot_api.reply_message(
                event.reply_token, TextSendMessage(text='發生錯誤！'))

    elif mtext == '@傳送門市位置':
        try:
            message = LocationSendMessage(
                title='101大樓',
                address='台北市信義路五段7號',
                latitude=25.034207,  # 緯度
                longitude=121.564590  # 經度
            )
            line_bot_api.reply_message(event.reply_token, message)
        except:
            line_bot_api.reply_message(
                event.reply_token, TextSendMessage(text='發生錯誤！'))


def sendCarousel(event):  # 轉盤樣板
    try:
        message = TemplateSendMessage(
            alt_text='轉盤樣板',
            template=CarouselTemplate(
                columns=[
                    CarouselColumn(
                        thumbnail_image_url='https://photo.sofun.tw/2017/04/Mo-PTT-Logo.png',
                        title='批踢踢',
                        text='請選擇看板',
                        actions=[
                            MessageTemplateAction(  # 顯示文字計息
                                label='八卦版',
                                text='@看八卦版'
                            ),
                            MessageTemplateAction(  # 顯示文字計息
                                label='表特版',
                                text='@看表特版'
                            ),
                            MessageTemplateAction(  # 顯示文字計息
                                label='批踢踢熱門文章',
                                text='@批踢踢熱門文章'
                            )
                        ]
                    ),
                    CarouselColumn(
                        thumbnail_image_url='https://icons-for-free.com/download-icon-forecast+partly+cloudy+weather+icon-1320196484400215944_512.png',
                        title='生活專區',
                        text='選擇項目',
                        actions=[
                            MessageTemplateAction(
                                label='查詢空氣品質',
                                text='@如何查詢空氣品質'
                            ),
                            MessageTemplateAction(
                                label='最近熱門電影',
                                text='@最近熱門電影'
                            ),
                            MessageTemplateAction(
                                label='今日運勢',
                                text='@看今日運勢'
                            )
                        ]
                    )
                ]
            )
        )
        line_bot_api.reply_message(event.reply_token, message)
    except:
        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text='發生錯誤！'))


def sendButton(event):
    try:
        message = TemplateSendMessage(
            alt_text='按鈕樣板',
            template=ButtonsTemplate(
                thumbnail_image_url='https://photo.sofun.tw/2017/04/Mo-PTT-Logo.png',  # 顯示的圖片
                title='批踢踢',  # 主標題
                text='請選擇：',  # 副標題
                actions=[
                    MessageTemplateAction(  # 顯示文字計息
                        label='八卦版',
                        text='@看八卦'
                    ),
                    MessageTemplateAction(  # 顯示文字計息
                        label='表特版',
                        text='@看表特'
                    ),
                    MessageTemplateAction(  # 顯示文字計息
                        label='找美食',
                        text='@找美食'
                    )
                ]
            )
        )
        line_bot_api.reply_message(event.reply_token, message)
    except:
        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text='發生錯誤！'))


def sendButton2(event):
    try:
        message = TemplateSendMessage(
            alt_text='按鈕樣板',
            template=ButtonsTemplate(
                thumbnail_image_url='https://media3.s-nbcnews.com/i/newscms/2018_21/2442281/og-nbcnews1200x630_c986de7e1bb6ad2281723b692aa61990.png',  # 顯示的圖片
                title='看新聞',
                text='請選擇：',
                actions=[
                    MessageTemplateAction(
                        label='國際新聞',
                        text='@看國際新聞'
                    ),
                    MessageTemplateAction(
                        label='國內新聞',
                        text='@看國內新聞'
                    )
                ]
            )
        )
        line_bot_api.reply_message(event.reply_token, message)
    except:
        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text='發生錯誤！'))


if __name__ == '__main__':
    app.run(port=2000)
