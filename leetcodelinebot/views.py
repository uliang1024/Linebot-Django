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
import schedule
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
                        reply_text = write_to_report_log(user_name=event.source.user_id, topic=topic, done=True)
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

def get_report_stats(user_id):
    taiwan_tz = pytz.timezone('Asia/Taipei')
    now = datetime.now(taiwan_tz)
    today = now.date()
    start_of_day = datetime.combine(today, datetime.min.time())
    end_of_day = datetime.combine(today, datetime.max.time())

    all_topics = ReportLog.objects(name=user_id).distinct("topic")
    total_count = len(all_topics)
    
    today_topics = ReportLog.objects(name=user_id, created_at__gte=start_of_day, created_at__lte=end_of_day).distinct("topic")
    today_count = len(today_topics)

    reply_text = f"過去總共完成了{total_count}題測驗，今日已完成{today_count}題"

    return reply_text

def extract_topic_from_message(message):
    # 刪除所有空格
    message = message.replace(" ", "")
    
    # 使用正則表達式提取數字部分
    match = re.search(r'完成(\d+)|(\d+)完成', message)
    
    if match:
        # 提取到數字部分，回傳作為 topic
        topic = match.group(1) or match.group(2)
        return topic
    
    # 若未提取到數字部分，回傳 None
    return None

def get_report_24_hours(user_id):
    taiwan_tz = pytz.timezone('Asia/Taipei')
    now = datetime.now(taiwan_tz)
    past_24_hours = now - timedelta(hours=24)

    past_24_hours_topics = ReportLog.objects(name=user_id, created_at__gte=past_24_hours).distinct("topic")
    past_24_hours_count = len(past_24_hours_topics)

    return past_24_hours_count

def remind_user():
    # 早上9點提醒，顯示過去24小時中每位使用者完成的題目總數
    # 若有使用者未達到2次，則在使用者名稱後面加上⚠️
    # 呼叫相應的函式來取得數據並組織回覆訊息
    # 使用 line_bot_api 調用 Line Bot API 來發送提醒訊息
    
    # 獲取所有使用者的名稱
    users = ReportLog.objects.distinct("name")
    
    reply_text = "過去24小時中：\n"
    
    for user in users:
        user_id = user.name
        count = get_report_24_hours(user_id)
        reply_text += f"{user_id}已完成{count}題"
        if count < 2:
            reply_text += " ⚠️"
        reply_text += "\n"
    
    # 發送提醒訊息給所有使用者
    for user in users:
        user_id = user.name
        line_bot_api.push_message(user_id, TextSendMessage(text=reply_text))

def remind_user_afternoon():
    # 下午3點提醒使用者請記得做 LeetCode 題目
    # 使用 line_bot_api 調用 Line Bot API 來發送提醒訊息
    
    # 獲取所有使用者的名稱
    users = ReportLog.objects.distinct("name")
    
    for user in users:
        user_id = user.name
        # 發送提醒訊息給使用者
        line_bot_api.push_message(user_id, TextSendMessage(text="請記得做 LeetCode 題目"))

def remind_user_evening():
    # 晚上9點提醒使用者請記得回報今日完成的題目
    # 使用 line_bot_api 調用 Line Bot API 來發送提醒訊息
    
    # 獲取所有使用者的名稱
    users = ReportLog.objects.distinct("name")
    
    for user in users:
        user_id = user.name
        # 發送提醒訊息給使用者
        line_bot_api.push_message(user_id, TextSendMessage(text="請記得回報今日完成的題目"))

# 設定排程任務
schedule.every().day.at("03:05").do(remind_user)
schedule.every().day.at("03:06").do(remind_user_afternoon)
schedule.every().day.at("03:07").do(remind_user_evening)

# 進入無限迴圈，持續執行排程任務
while True:
    schedule.run_pending()
    time.sleep(1)
