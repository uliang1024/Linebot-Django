from mongoengine import *
from django.utils import timezone

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
    created_at = DateTimeField(default=timezone.now)

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