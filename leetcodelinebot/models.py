from django.db import models

class ReportLog(models.Model):
    _id = models.CharField(max_length=50)
    name = models.CharField(max_length=50)
    done = models.BooleanField(default=False)
    _created_at = models.DateTimeField()
    _updated_at = models.DateTimeField()

    def __str__(self):
        return self.name