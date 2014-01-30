import datetime

from Child import Child

from django.db import models

from django.contrib.auth.models import User

class PsychologicalExamInfo(models.Model):
    child = models.ForeignKey(Child)
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