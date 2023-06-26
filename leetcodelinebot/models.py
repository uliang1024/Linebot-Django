from mongoengine import *

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
