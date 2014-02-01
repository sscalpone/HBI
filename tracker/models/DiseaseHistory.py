import datetime

from Child import Child

from django.db import models

from django.contrib.auth.models import User

class DiseaseHistory(models.Model):
    child = models.ForeignKey(Child)
    date = models.DateField()
    institution = models.CharField(max_length=200)
    diagnosis = models.TextField()
    studies = models.TextField()
    treatment = models.TextField()

    class Meta:
        app_label = 'tracker'
        db_table = 'tracker_diseasehistory'

