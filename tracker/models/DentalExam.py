import datetime

from Child import Child
from Signature import Signature

from django.db import models

from django.contrib.auth.models import User

class DentalExam(models.Model):
    child = models.ForeignKey(Child)
    signature = models.ForeignKey(Signature)
    date = models.DateField()
    diagnostico = models.TextField()
    recommendation = models.TextField()

    class Meta:
        app_label = 'tracker'
        db_table = 'tracker_dentalexam'

