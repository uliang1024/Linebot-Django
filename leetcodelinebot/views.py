from django.shortcuts import render
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings

from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import MessageEvent, TextSendMessage

from leetcodelinebot.models import write_to_report_log, get_report_stats, send_line_message, get_past_24_hours_stats, extract_topic_from_message

import pytz
import datetime
import time

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
                elif event.message.text.startswith('完成'):
                    topic = extract_topic_from_message(event.message.text)
                    if topic is not None:
                        # 建立 ReportLog 物件並保存到資料庫
                        user_id = event.source.user_id
                        profile = line_bot_api.get_profile(user_id)
                        print(profile)
                        reply_text = write_to_report_log(user_id=event.source.user_id, name=profile.displayName, topic=topic, done=True)
                        line_bot_api.reply_message(
                            event.reply_token,
                            TextSendMessage(text=reply_text)  # 回覆新增成功訊息
                        )
                    else:
                        line_bot_api.reply_message(
                            event.reply_token,
                            TextSendMessage(text='未提取到數字，舉例:[完成 1]')  # 回覆未提取到數字訊息
                        )
                    
        return HttpResponse()
    else:
        return HttpResponseBadRequest()

# while True:
#     # 获取当前台湾时间
#     tz = pytz.timezone('Asia/Taipei')
#     current_time = datetime.datetime.now().time()
#     trigger_time = datetime.time(4, 58)  # 设置触发时间为上午4点30分

#     if current_time.hour == trigger_time.hour and current_time.minute == trigger_time.minute:
#         reply_text = get_past_24_hours_stats() 
#         send_line_message(reply_text)
    
#     time.sleep(5)  # 每分钟检查一次时间