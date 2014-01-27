import datetime

from Child import Child

from django.db import models

from django.contrib.auth.models import User

class MedicalExamPart1Info(models.Model):
    child = models.ForeignKey(Child)
    date = models.DateField()
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

    class Meta:
        app_label = 'tracker'
        db_table = 'tracker_medicalexampart1info'
