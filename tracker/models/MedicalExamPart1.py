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
    bcg_vaccine = models.BooleanField()
    bcg_vaccine_date = models.DateField()
    polio_vaccine = models.BooleanField()
    polio_vaccine_date = models.DateField()
    dpt_vaccine = models.BooleanField()
    dpt_vaccine_date = models.DateField()
    hepatitis_b_vaccine = models.BooleanField()
    hepatitis_b_vaccine_date = models.DateField()
    flu_vaccine = models.BooleanField()
    flu_vaccine_date = models.DateField()
    yellow_fever_vaccine = models.BooleanField()
    yellow_fever_vaccine_date = models.DateField()
    spr_vaccine = models.BooleanField()
    spr_vaccine_date = models.DateField()
    hpv_vaccine = models.BooleanField()
    hpv_vaccine_date = models.DateField()
    pneumococcal_vaccine = models.BooleanField()
    pneumococcal_vaccine_date = models.DateField()
    weight = models.FloatField()
    height = models.FloatField()
    hemoglobin_normal = models.BooleanField()
    hemoglobin_notes = models.TextField()
    elisa_vh1_positive = models.BooleanField()
    hepatitisB_positive = models.BooleanField()
    PPD_positive = models.BooleanField()
    stool_parasites_positive = models.BooleanField()
    stool_parasites_notes = models.TextField()
    leukocytes_normal = models.BooleanField()
    leukocytes_notes = models.TextField()
    nitrites_normal = models.BooleanField()
    nitrites_notes = models.TextField()
    urobilinogen_normal = models.BooleanField()
    urobilinogen_notes = models.TextField()
    protein_normal = models.BooleanField()
    protein_notes = models.TextField()
    pH_normal = models.BooleanField()
    pH_notes = models.TextField()
    hemoglobin_normal = models.BooleanField()
    hemoglobin_notes = models.TextField()
    density_normal = models.BooleanField()
    density_notes = models.TextField()
    glucose_normal = models.BooleanField()
    glucose_notes = models.TextField()

    class Meta:
        app_label = 'tracker'
        db_table = 'tracker_medicalexampart1'

