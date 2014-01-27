import datetime

from django.db import models

from django.contrib.auth.models import User

class Residence(models.Model):
    residence_name = models.CharField(max_length=200)

    def __unicode__(self):
        return self.residence_name

    class Meta:
        app_label = 'tracker'
        db_table = 'tracker_residence'

