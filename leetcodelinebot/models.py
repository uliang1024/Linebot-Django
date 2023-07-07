from mongoengine import *

class Users(Document):
    user_id = StringField(required=True)
    display_name = StringField(default="")
    status_message = StringField(default="")
    picture_url = StringField(default="")
    punish = IntField(default=0)
    
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