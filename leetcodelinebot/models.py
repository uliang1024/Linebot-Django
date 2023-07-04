from mongoengine import *
from datetime import datetime
import pytz
import requests

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




def write_to_report_log(user_id, user_name, topic, done):
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
        name=user_name,
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