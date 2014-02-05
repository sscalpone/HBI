import datetime

from django.db import models

class Signature(models.Model):
    nombres = models.CharField(max_length=200)
    apellidos = models.CharField(max_length=200)
    emp = models.CharField(max_length=200)
    direccion = models.CharField(max_length=200)
    celular = models.CharField(max_length=200)

    class Meta:
        app_label = 'tracker'
        db_table = 'tracker_signature'

    def __unicode__(self):
        return self.nombres

