import datetime

from Child import Child
from Signature import Signature

from django.db import models

from django.contrib.auth.models import User

class MedicalExamPart2Info(models.Model):
    child = models.ForeignKey(Child)
    signature = models.ForeignKey(Signature)
    date = models.DateField()
    illness_notes = models.TextField()
    appetite_notes = models.TextField()
    sleep_notes = models.TextField()
    visual_acuity_right = models.CharField(max_length=200)
    visual_acuity_left = models.CharField(max_length=200)
    appearance_notes = models.TextField()
    skin_notes = models.TextField()
    lymph_notes = models.TextField()
    neck_notes = models.TextField()
    lung_notes = models.TextField()
    cardio_notes = models.TextField()
    abdomen_notes = models.TextField()
    genitourinary_notes = models.TextField()
    extremities_notes = models.TextField()
    neurological_notes = models.TextField()
    treatment_notes = models.TextField()
    recommendation = models.TextField()

    class Meta:
        app_label = 'tracker'
        db_table = 'tracker_medicalexampart2info'

class MedicalExamDiagnosis(models.Model):
    exam = models.ForeignKey(MedicalExamPart2Info)
    name = models.CharField(max_length=200)
    value = models.TextField()

    class Meta:
        app_label = 'tracker'
        db_table = 'tracker_medicalexamdiagnosis'
