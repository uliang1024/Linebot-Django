from django.db import models
from django_mongoengine import Document, fields

class ReportLog(Document):
    name = fields.StringField(required=True)
    done = fields.BooleanField(default=False)
    created_at = fields.DateTimeField(required=True)
    updated_at = fields.DateTimeField(required=True)

    meta = {
        'collection': 'ReportLog'  # 设置集合名称
    }