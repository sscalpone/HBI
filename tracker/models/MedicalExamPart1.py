import datetime

from Child import Child
from Signature import Signature

from django.db import models

from django.contrib.auth.models import User

class MedicalExamPart1(models.Model):
    child = models.ForeignKey(Child)
    date = models.DateField()
    background_notes = models.TextField()
    birth_history = models.TextField()
    bcg_vaccine = models.BooleanField(default=None)
    bcg_vaccine_date = models.DateField()
    polio_vaccine = models.BooleanField(default=None)
    polio_vaccine_date = models.DateField()
    dpt_vaccine = models.BooleanField(default=None)
    dpt_vaccine_date = models.DateField()
    hepatitis_b_vaccine = models.BooleanField(default=None)
    hepatitis_b_vaccine_date = models.DateField()
    flu_vaccine = models.BooleanField(default=None)
    flu_vaccine_date = models.DateField()
    yellow_fever_vaccine = models.BooleanField(default=None)
    yellow_fever_vaccine_date = models.DateField()
    spr_vaccine = models.BooleanField(default=None)
    spr_vaccine_date = models.DateField()
    hpv_vaccine = models.BooleanField(default=None)
    hpv_vaccine_date = models.DateField()
    pneumococcal_vaccine = models.BooleanField(default=None)
    pneumococcal_vaccine_date = models.DateField()
    weight = models.FloatField()
    height = models.FloatField()
    hemoglobin_normal = models.BooleanField(default=None)
    hemoglobin_notes = models.TextField()
    elisa_vh1_positive = models.BooleanField(default=None)
    hepatitisB_positive = models.BooleanField(default=None)
    PPD_positive = models.BooleanField(default=None)
    stool_parasites_positive = models.BooleanField(default=None)
    stool_parasites_notes = models.TextField()
    leukocytes_normal = models.BooleanField(default=None)
    leukocytes_notes = models.TextField()
    nitrites_normal = models.BooleanField(default=None)
    nitrites_notes = models.TextField()
    urobilinogen_normal = models.BooleanField(default=None)
    urobilinogen_notes = models.TextField()
    protein_normal = models.BooleanField(default=None)
    protein_notes = models.TextField()
    pH_normal = models.BooleanField(default=None)
    pH_notes = models.TextField()
    hemoglobin_normal = models.BooleanField(default=None)
    hemoglobin_notes = models.TextField()
    density_normal = models.BooleanField(default=None)
    density_notes = models.TextField()
    glucose_normal = models.BooleanField(default=None)
    glucose_notes = models.TextField()

    class Meta:
        app_label = 'tracker'
        db_table = 'tracker_medicalexampart1'

