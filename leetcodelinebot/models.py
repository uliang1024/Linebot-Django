from mongoengine import *

class Users(Document):
    user_id = StringField()
    name = StringField()
    status_message = StringField()
    picture_url = StringField()
    punish = IntField()
    created_at = DateTimeField()
    
    meta = {
        'collection': 'Users',
        'indexes': [
            'user_id',
            'name',
            'created_at' ,
        ],
        'ordering': ['user_id'],
        'strict': False 
    }
    
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
            'created_at',
        ],
        'ordering': ['created_at'],
        'strict': False 
    }