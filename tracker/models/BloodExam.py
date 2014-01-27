import datetime

from Child import Child

from django.db import models

from django.contrib.auth.models import User

class BloodExam(models.Model):
    child = models.ForeignKey(Child)
    date = models.DateField()
    hemogloban_normal = models.BooleanField()
    hemogloban_notes = models.TextField()
    elisa_vh1_normal = models.BooleanField()
    elisa_vh1_notes = models.TextField()
    hepatitis_b_normal = models.BooleanField()
    hepatitis_b_notes = models.TextField()
    ppd_normal = models.BooleanField()
    ppd_notes = models.TextField()
    orina_normal = models.BooleanField()
    orina_notes = models.TextField()
    white_cells_normal = models.BooleanField()
    white_cells_notes = models.TextField()
    nitrites_normal = models.BooleanField()
    nitrites_notes = models.TextField()
    urobilinogen_normal = models.BooleanField()
    urobilinogen_notes = models.TextField()
    protein_normal = models.BooleanField()
    protein_notes = models.TextField()
    ph_normal = models.BooleanField()
    ph_notes = models.TextField()
    density_normal = models.BooleanField()
    density_notes = models.TextField()
    glucoce_normal = models.BooleanField()
    glucoce_notes = models.TextField()

    class Meta:
        app_label = 'tracker'
        db_table = 'tracker_bloodexam'

class BloodParasite(models.Model):
    exam = models.ForeignKey(BloodExam)
    parasite = models.CharField(max_length=200)

    class Meta:
        app_label = 'tracker'
        db_table = 'tracker_bloodparasite'

