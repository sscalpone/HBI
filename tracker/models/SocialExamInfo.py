import datetime

from Child import Child

from django.db import models

from django.contrib.auth.models import User

class SocialExamInfo(models.Model):
    child = models.ForeignKey(Child)
    date = models.DateField()
    has_birth_certificate = models.BooleanField()
    original_birth_certificate = models.BooleanField()
    dni = models.BooleanField()
    dni_in_process = models.BooleanField()
    dni_comments = models.TextField()
    sis = models.BooleanField()
    sis_in_process = models.BooleanField()
    sis_comments = models.TextField()
    antecedents = models.TextField()
    family_situation = models.TextField()
    health_situation = models.TextField()
    housing_situation = models.TextField()
    economic_situation = models.TextField()
    general_comments = models.TextField()
    visitors_allowed = models.BooleanField()
    visitors_notes = models.TextField()
    social_diagnosis = models.TextField()
    recommendation = models.TextField()

    class Meta:
        app_label = 'tracker'
        db_table = 'tracker_socialexaminfo'
