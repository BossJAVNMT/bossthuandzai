import json
import aiohttp
from os import environ
from aiohttp import web
import requests
import math
from datetime import datetime
from datetime import time
from datetime import date

# fanpage token
PAGE_ACCESS_TOKEN = 'EAAjtNWoSWWkBABK3SZBB5mxLe9eDw7s5YRk3Yg9HNKZCqZBmoiZAZBIXZBXBhXOtgsfCkcaYas22iSNhFVswPrYw421JKjiD4mqRLx9ZA99t9so0kKqklPoZBYdagmR6X2KPBnGwXDcEnMmz99qZB7g1UeOPJSESkEZC5NrOSl9RGU7KFkUdoKVvd3'
# verify token
VERIFY_TOKEN = 'thuandzai'

class BotControl(web.View):

    async def get(self):
        query = self.request.rel_url.query
        if(query.get('hub.mode') == "subscribe" and query.get("hub.challenge")):
            if not query.get("hub.verify_token") == VERIFY_TOKEN:
                return web.Response(text='Verification token mismatch', status=403)
            return web.Response(text=query.get("hub.challenge"))
        return web.Response(text='Forbidden', status=403)

    async def post(self):
        data = await self.request.json()
        if data.get("object") == "page":
            await self.send_greeting("Chào bạn. Mình là bot demo của Ngô Thuận.")

            for entry in data.get("entry"):
                for messaging_event in entry.get("messaging"):
                    if messaging_event.get("message"):
                        sender_id = messaging_event["sender"]["id"]
                        message_text = messaging_event["message"]["text"]
                        #xác định giờ-thứ-ngày-tháng-năm
                        today = date.today()
                        weekday = ['THỨ 2','THỨ 3','THỨ 4','THỨ 5','THỨ 6','THỨ 7']
                        thu = today.weekday()
                        ngay = today.day
                        
                        #Thời khóa biểu
                        if any(["thời khóa biểu" in message_text.lower(), "tkb" in message_text.lower()]):
                            urltkb = 'https://bonded-halts.000webhostapp.com/TKB.json'
                            geturltkb = requests.get(urltkb).json()
                            const = len(geturltkb)
                            for i in range(const):
                               await self.send_message(sender_id, geturltkb[i][weekday[thu]])
                        #lịch tháng 6
                        elif any(["lịch hôm nay" in message_text.lower(), "lịch trình" in message_text.lower()]):
                            #get tháng 6
                            urlt6 = 'https://bonded-halts.000webhostapp.com/thang6.json'
                            geturlt6 = requests.get(urlt6).json()
                            constt6 = len(geturlt6['Trang tính1'])
                            ngayjson = ngay - 1
                            sang = geturlt6['Trang tính1'][ngayjson]['Sáng']
                            chieu = geturlt6['Trang tính1'][ngayjson]['Chiều']
                            toi = geturlt6['Trang tính1'][ngayjson]['Tối']

                            #Kiểm tra môn học
                            Monhoc = {'TT':'Học Trên Trường','HH':'19h-Học Hóa Anh Hậu','TA':'18h-Học Tiếng Anh Chị Phương','HT':'Học Toán Thầy Đông'}
                            if sang == None:
                                hocsang = 'Sáng nay bạn được nghỉ !'
                            else:
                                hocsang = 'Sáng Nay Bạn ' + Monhoc[sang]

                            if chieu == None:
                                hocchieu = 'Chiều nay bạn được nghỉ !'
                            else:
                                hocchieu = 'Chiều Nay Bạn ' + Monhoc[chieu]

                            if toi == None:
                                hoctoi = 'Tối nay bạn được nghỉ !'
                            else:
                                hoctoi = 'Tối Nay Bạn ' + Monhoc[toi]
                            #gửi
                            await self.send_message(sender_id, hocsang)
                            await self.send_message(sender_id, hocchieu)
                            await self.send_message(sender_id, hoctoi)

                        #rep ib thường
                        elif any(["hello" in message_text.lower(), "chào" in message_text.lower(), "hi" in message_text.lower(),
                            "alo" in message_text.lower(), "ơi" in message_text.lower()]):
                            await self.send_message(sender_id, 'Chào Bạn :)')
                        elif any(["ai tạo" in message_text.lower(), "ai sáng lập" in message_text.lower(), "ai lập trình" in message_text.lower(),
                            "bạn là gì" in message_text.lower(), "mày là gì" in message_text.lower()]):                               
                            await self.send_message(sender_id, 'Mình là Chatbot được lập trình bằng ngôn ngữ python')
                            await self.send_message(sender_id, 'Ngô Thuận Dzai Đã Tạo Ra Mình <3')
                        
                        #chat bot không hiểu
                        else:
                            await self.send_message(sender_id, "Bạn dễ thương gì ấy ơi, Bạn Nói Gì Mình Không Hiểu ?")
                            await self.send_message(sender_id,
                                              "Do Bố Mình Lập Trình Nên Vẫn Còn Thiếu Sót, và sẽ bổ sung thêm ạ,Thank iu <3")

        return web.Response(text='ok', status=200)

    async def send_greeting(self, message_text):
        params = {
            "access_token": PAGE_ACCESS_TOKEN
        }
        headers = {
            "Content-Type": "application/json"
        }
        data = json.dumps({
            "setting_type": "greeting",
            "greeting": {
                "text": message_text
            }
        })
        async with aiohttp.ClientSession() as session:
            await session.post("https://graph.facebook.com/v3.0/me/thread_settings", params=params, headers=headers, data=data)

    async def send_message(self, sender_id, message_text):

        params = {
            "access_token": PAGE_ACCESS_TOKEN
        }
        headers = {
            "Content-Type": "application/json"
        }
        data = json.dumps({
            "recipient": {
                "id": sender_id
            },
            "message": {
                "text": message_text
            }
        })

        async with aiohttp.ClientSession() as session:
            await session.post("https://graph.facebook.com/v3.0/me/messages", params=params, headers=headers, data=data)



routes = [
    web.get('/', BotControl, name='verify'),
    web.post('/', BotControl, name='webhook'),
]

app = web.Application()
app.add_routes(routes)

#if __name__ == '__main__':
    #web.run_app(app, host='0.0.0.0', port=environ.get("PORT", 9090))
