# coding=utf-8

import datetime

from django.contrib.auth.models import User
from django.db import models
from django.forms import ModelForm

from Child import Child
from Signature import Signature
from MedicalExamPart2 import MedicalExamPart2

class CurrentMedsList(models.Model):
    child = models.ForeignKey(Child)
    exam = models.ForeignKey(MedicalExamPart2, blank=True, null=True)
    med_name = models.CharField(max_length=200, blank=True, null=True)
    dose = models.CharField(max_length=200, blank=True, null=True)
    frequency = models.CharField(max_length=200, blank=True, null=True)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    signature = models.ForeignKey(Signature, blank=True, null=True)

    class Meta:
        app_label = 'tracker'
        db_table = 'tracker_currentmedslist'

class CurrentMedsListForm(ModelForm):
    class Meta:
        model = CurrentMedsList
        fields = (
            'med_name',
            'dose',
            'frequency',
            'start_date',
            'end_date',
        )
        labels = {
            'med_name': 'Nombre del Medicamento',
            'dose': 'Dosis',
            'frequency': 'Frecuencia',
            'start_date': 'Fecha de Inicio',
            'end_date': 'Fecha Final'
        }

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(CurrentMedsListForm, self).__init__(*args, **kwargs)

    def clean(self):
        msg = "Este campo es obligatorio."
        cleaned_data = super(CurrentMedsListForm, self).clean()

        if self.request.POST:
            if 'submit' in self.request.POST:
                med_name = cleaned_data.get('med_name')
                dose = cleaned_data.get('dose')
                if med_name!='' and dose=='':
                    self.add_error('dose', msg)
                frequency = cleaned_data.get('frequency')
                if med_name!='' and frequency=='':
                    self.add_error('frequency', msg)
                start_date = cleaned_data.get('start_date')
                if med_name!='' and start_date=='':
                    self.add_error('start_date',)
                end_date = cleaned_data.get('end_date')
                if med_name!='' and end_date=='':
                    self.add_error('end_date', msg)


class PastMedsList(models.Model):
    child = models.ForeignKey(Child)
    exam = models.ForeignKey(MedicalExamPart2, blank=True, null=True)
    med_name = models.CharField(max_length=200, blank=True, null=True)
    dose = models.CharField(max_length=200, blank=True, null=True)
    frequency = models.CharField(max_length=200, blank=True, null=True)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    signature = models.ForeignKey(Signature, blank=True, null=True)

    class Meta:
        app_label = 'tracker'
        db_table = 'tracker_pastmedslist'


class PastMedsListForm(ModelForm):
    class Meta:
        model = PastMedsList
        fields = (
            'med_name',
            'dose',
            'frequency',
            'start_date',
            'end_date',
        )
        labels = {
            'med_name': 'Nombre del Medicamento',
            'dose': 'Dosis',
            'frequency': 'Frecuencia',
            'start_date': 'Fecha de Inicio',
            'end_date': 'Fecha Final'
        }

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(PastMedsListForm, self).__init__(*args, **kwargs)

    def clean(self):
        msg = "Este campo es obligatorio."
        cleaned_data = super(PastMedsListForm, self).clean()
        if self.request.POST:
            if 'submit' in self.request.POST:
                med_name = cleaned_data.get('med_name')
                dose = cleaned_data.get('dose')
                if med_name!='' and dose=='':
                    self.add_error('dose', msg)
                frequency = cleaned_data.get('frequency')
                if med_name!='' and frequency=='':
                    self.add_error('frequency', msg)
                start_date = cleaned_data.get('start_date')
                if med_name!='' and start_date=='':
                    self.add_error('start_date',)
                end_date = cleaned_data.get('end_date')
                if med_name!='' and end_date=='':
                    self.add_error('end_date', msg)




