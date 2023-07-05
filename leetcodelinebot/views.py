from django.shortcuts import render
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings

from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import MessageEvent, TextSendMessage

from leetcodelinebot.models import write_to_report_log, get_report_stats, send_line_message, get_past_24_hours_stats, extract_topic_from_message, settlement_event, reminder_event, report_event

import datetime
import time
import pytz

line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)
parser = WebhookParser(settings.LINE_CHANNEL_SECRET)

@csrf_exempt
def callback(request):
    if request.method == 'POST':
        signature = request.META['HTTP_X_LINE_SIGNATURE']
        body = request.body.decode('utf-8')
 
        try:
            events = parser.parse(body, signature)  # 傳入的事件
        except InvalidSignatureError:
            return HttpResponseForbidden()
        except LineBotApiError:
            return HttpResponseBadRequest()
 
        for event in events:
            if isinstance(event, MessageEvent):  # 如果有訊息事件
                if event.message.text == '查詢紀錄':
                    user_id = event.source.user_id
                    reply_text = get_report_stats(user_id)  # 呼叫函式取得 ReportLog 統計數據
                    line_bot_api.reply_message(
                        event.reply_token,
                        TextSendMessage(text=reply_text)  # 構建回覆訊息
                    )
                elif event.message.text is not None and event.message.text.startswith('完成'):
                    topic = extract_topic_from_message(event.message.text)
                    if topic is not None:
                        # 建立 ReportLog 物件並保存到資料庫
                        user_id = event.source.user_id
                        profile = line_bot_api.get_profile(user_id)
                        reply_text = write_to_report_log(user_id=event.source.user_id, name=profile.display_name, topic=topic, done=True)
                        line_bot_api.reply_message(
                            event.reply_token,
                            TextSendMessage(text=reply_text)  # 回覆新增成功訊息
                        )
                    else:
                        line_bot_api.reply_message(
                            event.reply_token,
                            TextSendMessage(text='未提取到數字，舉例:[完成 1]')  # 回覆未提取到數字訊息
                        )
                elif event.message.text == '測試':
                    text = get_past_24_hours_stats() 
                    send_line_message(text)
                    
        return HttpResponse()
    else:
        return HttpResponseBadRequest()

# 设置台湾时区
taipei_tz = pytz.timezone('Asia/Taipei')

while True:
    now = datetime.datetime.now(taipei_tz)
    
    # 检查当前时间是否是早上八点、下午两点或晚上十点
    if now.hour == 17 and now.minute == 13 and now.second == 0:
        text = settlement_event() 
        send_line_message(text)
    elif now.hour == 17 and now.minute == 14 and now.second == 0:
        text = reminder_event()
        send_line_message(text)
    elif now.hour == 17 and now.minute == 22 and now.second == 0:
        text = report_event()
        send_line_message(text)
    
    # 等待1秒钟，避免频繁检查
    time.sleep(1)