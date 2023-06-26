from django.shortcuts import render
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
 
from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import MessageEvent, TextSendMessage

from leetcodelinebot.models import ReportLog, write_to_report_log
from datetime import datetime, timedelta

import pytz
import re

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
                        write_to_report_log(user_name=event.source.user_id, topic=topic, done=True)
                        line_bot_api.reply_message(
                            event.reply_token,
                            TextSendMessage(text='已新增 ReportLog 資料')  # 回覆新增成功訊息
                        )
                    else:
                        line_bot_api.reply_message(
                            event.reply_token,
                            TextSendMessage(text='未提取到數字部分，舉例：[完成 1]')  # 回覆未提取到數字訊息
                        )
                    
        return HttpResponse()
    else:
        return HttpResponseBadRequest()

def get_report_stats(user_id):
    taiwan_tz = pytz.timezone('Asia/Taipei')
    now = datetime.now(taiwan_tz)
    today = now.date()
    start_of_day = datetime.combine(today, datetime.min.time())
    end_of_day = datetime.combine(today, datetime.max.time())

    all_logs = ReportLog.objects(name=user_id).distinct("topic")
    total_count = ReportLog.objects(name=user_id).count()
    today_count = ReportLog.objects(name=user_id, created_at__gte=start_of_day, created_at__lte=end_of_day).count()

    reply_text = f"過去總共完成了{total_count}題測驗，今日已完成{today_count}題"

    return reply_text

def extract_topic_from_message(message):
    # 使用正則表達式提取數字部分
    match = re.search(r'\b完成\s+(\d+)\b', message)
    
    if match:
        # 提取到數字部分，回傳作為 topic
        topic = match.group(1)
        return topic
    
    # 若未提取到數字部分，回傳 None
    return None