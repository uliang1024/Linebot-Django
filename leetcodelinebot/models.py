from mongoengine import *
from datetime import datetime, timedelta
import pytz
import re
from pytz import timezone
import requests
from django.conf import settings

from linebot import LineBotApi

line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)

class ReportLog(Document):
    user_id = StringField()
    name = StringField()
    topic = StringField()
    done = BooleanField()
    created_at = DateTimeField()

    meta = {
        'collection': 'ReportLog',
        'indexes': [
            'user_id',
            'name',
            'topic',
            'created_at',
        ],
        'ordering': ['created_at'],
        'strict': False 
    }




def write_to_report_log(user_id, name, topic, done):
    # 检查是否已存在相同用户和相同topic的记录
    existing_log = ReportLog.objects(user_id=user_id, topic=topic).first()

    if existing_log:
        # 若已存在记录，回复相应消息
        reply_text = f"第{topic}题您已经完成了，请换个题目"
        return reply_text

    # 取得当前的台湾时间
    taiwan_tz = pytz.timezone('Asia/Taipei')
    taiwan_time = datetime.now(taiwan_tz)

    # 创建ReportLog对象并设置属性值
    report_log = ReportLog(
        user_id=user_id,
        name=name,
        topic=topic,
        done=done,
        created_at=taiwan_time
    )

    # 储存ReportLog对象到数据库
    report_log.save()
    reply_text = f"已新增ReportLog数据 {taiwan_time.strftime('%m/%d %H:%M')}"
    return reply_text


def send_line_message(message):
    url = "https://notify-api.line.me/api/notify"
    headers = {
        "Authorization": "Bearer " + '3t3o0JGWlcQfcv21kc4IBdM6uyyPlVhBSgxQOZTFNUM',
        "Content-Type": "application/x-www-form-urlencoded"
    }
    params = {
        'message': message
    }
    response = requests.post(url, headers=headers, params=params)
    if response.status_code == 200:
        print("Line message sent successfully.")
    else:
        print("Failed to send Line message.")
        
def get_past_24_hours_stats():
    # 取得台灣時區
    taiwan_tz = timezone('Asia/Taipei')
    # 取得過去24小時的起始時間和結束時間
    start_time = datetime.now(taiwan_tz) - timedelta(hours=24)
    end_time = datetime.now(taiwan_tz)
    
    # 查詢過去24小時內完成題目的使用者和題目數量
    result = ReportLog.objects(created_at__gte=start_time, created_at__lt=end_time).aggregate([
        {"$group": {"_id": "$name", "count": {"$sum": 1}}}
    ])
    
    reply_text = ""
    
    for entry in result:
        user_id = entry["_id"]
        count = entry["count"]
        
        # 構建回覆訊息
        reply_text += f"{user_id}：{count} 題\n"
    
    reply_text += '請繼續完成今日的進度。'
    
    return reply_text


def get_report_stats(user_id):
    taiwan_tz = pytz.timezone('Asia/Taipei')
    now = datetime.now(taiwan_tz)
    today = now.date()
    start_of_day = datetime.combine(today, datetime.min.time())
    end_of_day = datetime.combine(today, datetime.max.time())

    all_topics = ReportLog.objects(user_id=user_id).distinct("topic")
    total_count = len(all_topics)
    
    today_topics = ReportLog.objects(user_id=user_id, created_at__gte=start_of_day, created_at__lte=end_of_day).distinct("topic")
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