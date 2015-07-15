import datetime
from Child import Child

from django.db import models

from django.contrib.auth.models import User

class BasicInfo(models.Model):
    child = models.ForeignKey(Child)

    class Meta:
        app_label = 'tracker'
        db_table = 'tracker_basicinfo'

