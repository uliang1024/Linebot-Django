from mongoengine import *
from django.utils import timezone
from datetime import datetime

class Users(Document):
    user_id = StringField(required=True)
    display_name = StringField()
    status_message = StringField()
    picture_url = StringField()
    punish = IntField(default=0)
    
class ReportLog(Document):
    user_id = StringField()
    name = StringField()
    topic = StringField()
    done = BooleanField()
    taiwan_tz = timezone('Asia/Taipei')
    taiwan_time = datetime.now(taiwan_tz)
    created_at = DateTimeField(default=taiwan_time)

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