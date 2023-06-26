from mongoengine import *
from datetime import datetime

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
    # 創建 ReportLog 物件並設定屬性值
    report_log = ReportLog(
        name=user_name,
        topic=topic,
        done=done,
        created_at=datetime.now()
    )
    
    # 儲存 ReportLog 物件到資料庫
    report_log.save()