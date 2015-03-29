import datetime

from Child import Child
from Signature import Signature

from django.db import models

from django.contrib.auth.models import User

class DentalExam(models.Model):
    child = models.ForeignKey(Child)
    date = models.DateField()
    recommendation = models.TextField()

    class Meta:
        app_label = 'tracker'
        db_table = 'tracker_dentalexam'

class DentalExamDiagnosis(models.Model):
    exam = models.ForeignKey(DentalExam)
    diagnosis_notes = models.TextField()

    class Meta:
        app_label = 'tracker'
        db_table = 'tracker_dentalexamdiagnosis'

