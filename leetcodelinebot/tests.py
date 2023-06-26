from django.test import TestCase
from mongoengine import *

connect("linebot", host="mongodb+srv://amisleo000:AMISleo123@cluster0.3dwwur1.mongodb.net")

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
# 获取所有 ReportLog 文档
all_logs = ReportLog.objects.all()

# 遍历并输出文档数据
for log in all_logs:
    print(log.name, log.topic, log.done, log.created_at)