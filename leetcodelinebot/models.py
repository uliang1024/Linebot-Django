from django_mongoengine import Document, fields

class ReportLog(Document):
    name = fields.StringField(max_length=255)
    Done = fields.BooleanField()