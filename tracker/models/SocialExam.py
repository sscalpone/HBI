import datetime

from Child import Child
from Signature import Signature

from django.db import models

from django.contrib.auth.models import User

class SocialExam(models.Model):
    child = models.ForeignKey(Child)
    date = models.DateField()
    has_birth_certificate = models.BooleanField()
    original_birth_certificate = models.BooleanField()
    dni = models.BooleanField()
    dni_in_process = models.BooleanField()
    dni_no_comments = models.TextField(blank=True)
    sis = models.BooleanField()
    sis_in_process = models.BooleanField()
    sis_no_comments = models.TextField(blank=True)
    antecedents = models.TextField()
    family_situation = models.TextField()
    health_situation = models.TextField()
    housing_situation = models.TextField()
    economic_situation = models.TextField()
    general_comments = models.TextField()
    visitors_allowed = models.BooleanField()
    visitors_allowed_no_comments = models.TextField(blank=True)
    social_diagnosis = models.TextField()
    recommendation = models.TextField()

    class Meta:
        app_label = 'tracker'
        db_table = 'tracker_socialexam'
