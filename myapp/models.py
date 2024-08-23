from django.db import models
from datetime import datetime

class DataItem(models.Model):
    content = models.CharField(max_length=200)
    timestamp = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return self.content
