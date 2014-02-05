import datetime

from Child import Child
from Signature import Signature

from django.db import models

class PsychologicalExamInfo(models.Model):
    child = models.ForeignKey(Child)
    signature = models.ForeignKey(Signature)
    date = models.DateField()
    family_notes = models.TextField()
    physical_description = models.TextField()
    intelectual_notes = models.TextField()
    organicity_notes = models.TextField()
    psychomotor_notes = models.TextField()
    emotional_notes = models.TextField()
    recommendation = models.TextField()

    class Meta:
        app_label = 'tracker'
        db_table = 'tracker_psychologicalexaminfo'

class PsychologicalExamDiagnosis(models.Model):
    title = models.CharField(max_length=200)
    dwmq = models.CharField(max_length=200)
    exam = models.ForeignKey(PsychologicalExamInfo)

    class Meta:
        app_label = 'tracker'
        db_table = 'tracker_psychologicalexamdiagnosis'
