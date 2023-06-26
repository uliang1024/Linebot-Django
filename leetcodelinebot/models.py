from mongoengine import *
from datetime import datetime
import pytz

class ReportLog(Document):
    name = StringField()
    topic = StringField()
    done = BooleanField()
    created_at = DateTimeField()

    meta = {
        'collection': 'ReportLog',
        'indexes': [
            # 定义索引（可选）
            'name',
            'topic',
            'created_at',
        ],
        'ordering': ['created_at'],
        'strict': False 
    }



def write_to_report_log(user_name, topic, done):
    # 檢查是否已存在相同使用者和相同 topic 的紀錄
    existing_log = ReportLog.objects(name=user_name, topic=topic).first()

    if existing_log:
        # 若已存在紀錄，回覆相應訊息
        reply_text = f"第{topic}題您已經完成了，請換個題目"
        return reply_text
    
    # 取得當前的台灣時間
    taiwan_tz = pytz.timezone('Asia/Taipei')
    taiwan_time = datetime.now(taiwan_tz)
    
    # 創建 ReportLog 物件並設定屬性值
    report_log = ReportLog(
        name=user_name,
        topic=topic,
        done=done,
        created_at=taiwan_time
    )
    
    # 儲存 ReportLog 物件到資料庫
    report_log.save()
    reply_text = f"已新增 ReportLog 資料"
    return reply_text
