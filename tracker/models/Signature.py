import datetime

from django.db import models

from django.forms import ModelForm

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

class SignatureForm(ModelForm):
    class Meta:
        model = Signature
        fields = (
            'name',
            'surname',
            'emp',
            'direction',
            'cell',
        )
        labels = {
            'name': 'Nombres',
            'surname': 'Apellidos',
            'emp': 'EMP',
            'direction': 'Direccion',
            'cell': 'Celular',
        }