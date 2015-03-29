import datetime

from Child import Child
from Signature import Signature

from django.db import models

from django.contrib.auth.models import User

class MedicalExamPart2(models.Model):
    child = models.ForeignKey(Child)
    date = models.DateField()
    illness_notes = models.TextField()
    appetite_notes = models.TextField()
    sleep_notes = models.TextField()
    concerns_notes = models.TextField()
    blood_pressure = models.TextField()
    pulse = models.TextField()
    visual_acuity_left = models.TextField()
    visual_acuity_right = models.TextField()
    appearance_normal = models.BooleanField()
    appearance_notes = models.TextField()
    skin_mucosa_normal = models.BooleanField()
    skin_mucosa_notes = models.TextField()
    TCSC_lymph_normal = models.BooleanField()
    TCSC_lymph_notes = models.TextField()
    head_neck_normal = models.BooleanField()
    head_neck_notes = models.TextField()
    thorax_lungs_normal = models.BooleanField()
    thorax_lungs_notes = models.TextField()
    cardio_normal = models.BooleanField()
    cardio_notes = models.TextField()
    abdomen_normal = models.BooleanField()
    abdomen_notes = models.TextField()
    genitourinary_normal = models.BooleanField()
    genitourinary_notes = models.TextField()
    extremities_normal = models.BooleanField()
    extremities_notes = models.TextField()
    neurological_normal = models.BooleanField()
    neurological_notes = models.TextField()
    recommendations = models.TextField()

    class Meta:
        app_label = 'tracker'
        db_table = 'tracker_medicalexampart2'

class CurrentMedsList(models.Model):
    exam = models.ForeignKey(MedicalExamPart2)
    med_name = models.TextField()
    dose = models.TextField()
    frequency = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()

    class Meta:
        app_label = 'tracker'
        db_table = 'tracker_currentmedslist'

class PastMedsList(models.Model):
    exam = models.ForeignKey(MedicalExamPart2)
    med_name = models.TextField()
    dose = models.TextField()
    frequency = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()

    class Meta:
        app_label = 'tracker'
        db_table = 'tracker_pastmedslist'

class MedicalExamDiagnosis(models.Model):
    exam = models.ForeignKey(MedicalExamPart2)
    name = models.TextField()
    value = models.TextField()

    class Meta:
        app_label = 'tracker'
        db_table = 'tracker_medicalexamdiagnosis'

