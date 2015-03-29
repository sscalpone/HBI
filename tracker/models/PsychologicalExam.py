import datetime

from Child import Child
from Signature import Signature

from django.db import models

class PsychologicalExam(models.Model):
    child = models.ForeignKey(Child)
    date = models.DateField()
    background_notes = models.TextField()
    physical_description = models.TextField()
    intelectual_notes = models.TextField()
    organicity_notes = models.TextField()
    psychomotor_notes = models.TextField()
    emotional_notes = models.TextField()
    recommendation = models.TextField()

    class Meta:
        app_label = 'tracker'
        db_table = 'tracker_psychologicalexam'

class PsychologicalExamDiagnosis(models.Model):
    exam = models.ForeignKey(PsychologicalExam)
    diagnoses = models.TextField()
    diagnoses_cie_dsm9 = models.TextField()

    class Meta:
        app_label = 'tracker'
        db_table = 'tracker_psychologicalexamdiagnosis'
