import datetime

from django.db import models

class Signature(models.Model):
    name = models.CharField(max_length=200)
    surname = models.CharField(max_length=200)
    emp = models.CharField(max_length=200)
    direction = models.CharField(max_length=200)
    cell = models.CharField(max_length=200)

    class Meta:
        app_label = 'tracker'
        db_table = 'tracker_signature'

    def __unicode__(self):
        return self.name

