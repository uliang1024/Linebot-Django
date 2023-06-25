from django_mongoengine import Document, fields

class ReportLog(Document):
    _id = fields.StringField(max_length=255)
    name = fields.StringField(max_length=255)
    Done = fields.BooleanField()
    _created_at = fields.DateTimeField()
    _updated_at = fields.DateTimeField()