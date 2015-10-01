# coding=utf-8

import datetime

from django.contrib.auth.models import User
from django.db import models
from django.forms import ModelForm
from django.forms import RadioSelect

from Child import Child
from Signature import Signature

class MedicalExamPart1(models.Model):
    child = models.ForeignKey(Child)
    date = models.DateField()
    background_notes = models.TextField(blank=True, null=True) #not in schema
    birth_history = models.TextField(blank=True, null=True) #not in schema
    bcg_vaccine = models.BooleanField(default=False)
    bcg_vaccine_date = models.DateField(blank=True, null=True)
    polio_vaccine = models.BooleanField(default=False)
    polio_vaccine_date = models.DateField(blank=True, null=True)
    dpt_vaccine = models.BooleanField(default=False)
    dpt_vaccine_date = models.DateField(blank=True, null=True)
    hepatitis_b_vaccine = models.BooleanField(default=False)
    hepatitis_b_vaccine_date = models.DateField(blank=True, null=True)
    flu_vaccine = models.BooleanField(default=False)
    flu_vaccine_date = models.DateField(blank=True, null=True)
    yellow_fever_vaccine = models.BooleanField(default=False)
    yellow_fever_vaccine_date = models.DateField(blank=True, null=True)
    spr_vaccine = models.BooleanField(default=False)
    spr_vaccine_date = models.DateField(blank=True, null=True)
    hpv_vaccine = models.BooleanField(default=False)
    hpv_vaccine_date = models.DateField(blank=True, null=True)
    pneumococcal_vaccine = models.BooleanField(default=False)
    pneumococcal_vaccine_date = models.DateField(blank=True, null=True)
    weight = models.FloatField(blank=True, null=True)
    height = models.FloatField(blank=True, null=True)
    signature = models.ForeignKey(Signature, blank=True, null=True)

    class Meta:
        app_label = 'tracker'
        db_table = 'tracker_medicalexampart1'

class Growth(models.Model):
    child = models.ForeignKey(Child)
    exam = models.ForeignKey(MedicalExamPart1)
    date = models.DateField()
    height = models.FloatField(blank=True, null=True)
    weight = models.FloatField(blank=True, null=True)
    age = models.FloatField(blank=True, null=True)
    gender = models.CharField(max_length=6, blank=True, null=True)


class MedicalExamPart1Form(ModelForm):
    class Meta:
        model = MedicalExamPart1
        fields = (
            'date',
            'background_notes',
            'birth_history',
            'bcg_vaccine',
            'bcg_vaccine_date',
            'polio_vaccine',
            'polio_vaccine_date',
            'dpt_vaccine',
            'dpt_vaccine_date',
            'hepatitis_b_vaccine',
            'hepatitis_b_vaccine_date',
            'flu_vaccine',
            'flu_vaccine_date',
            'yellow_fever_vaccine',
            'yellow_fever_vaccine_date',
            'spr_vaccine',
            'spr_vaccine_date',
            'hpv_vaccine',
            'hpv_vaccine_date',
            'pneumococcal_vaccine',
            'pneumococcal_vaccine_date',
            'weight',
            'height',
        )
        labels = {
            'date': 'Fecha',
            'background_notes': 'Antecedents Familiares Patologicos y de Riesgo Conocidos',
            'birth_history': 'Historia Perinatal y Neonatal',
            'bcg_vaccine': 'BCG',
            'bcg_vaccine_date': 'Fecha de Administracion',
            'polio_vaccine': 'Antipoliomielitica',
            'polio_vaccine_date': 'Fecha de Administracion',
            'dpt_vaccine': 'DPT',
            'dpt_vaccine_date': 'Fecha de Administracion',
            'hepatitis_b_vaccine': 'Hepatitis B',
            'hepatitis_b_vaccine_date': 'Fecha de Administracion',
            'flu_vaccine': 'Hemofilus Influenza',
            'flu_vaccine_date': 'Fecha de Administracion',
            'yellow_fever_vaccine': 'Fiebre Amarilla',
            'yellow_fever_vaccine_date': 'Fecha de Administracion',
            'spr_vaccine': 'SPR',
            'spr_vaccine_date': 'Fecha de Administracion',
            'hpv_vaccine': 'HPV',
            'hpv_vaccine_date': 'Fecha de Administracion',
            'pneumococcal_vaccine': 'Neumococo',
            'pneumococcal_vaccine_date': 'Fecha de Administracion',
            'weight': 'Peso (kg)',
            'height': 'Estatura (cm)',
        }
        widgets = {
            'bcg_vaccine': RadioSelect(choices=((True, 'Si'),(False, 'No'))),
            'polio_vaccine': RadioSelect(choices=((True, 'Si'),(False, 'No'))),
            'dpt_vaccine': RadioSelect(choices=((True, 'Si'),(False, 'No'))),
            'hepatitis_b_vaccine': RadioSelect(choices=((True, 'Si'),(False, 'No'))),
            'flu_vaccine': RadioSelect(choices=((True, 'Si'),(False, 'No'))),
            'yellow_fever_vaccine': RadioSelect(choices=((True, 'Si'),(False, 'No'))),
            'spr_vaccine': RadioSelect(choices=((True, 'Si'),(False, 'No'))),
            'hpv_vaccine': RadioSelect(choices=((True, 'Si'),(False, 'No'))),
            'pneumococcal_vaccine': RadioSelect(choices=((True, 'Si'),(False, 'No'))),
        }

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(MedicalExamPart1Form, self).__init__(*args, **kwargs)

    def clean(self):
        msg = "Este campo es obligatorio."
        cleaned_data = super(MedicalExamPart1Form, self).clean()

        if self.request.POST:
            if 'submit' in self.request.POST:

                background_notes = cleaned_data.get('background_notes')
                if background_notes=='':
                    self.add_error('background_notes', msg)

                birth_history = cleaned_data.get('birth_history')
                if birth_history=='':
                    self.add_error('birth_history', msg)

                weight = cleaned_data.get('weight')
                if weight is None:
                    self.add_error('weight', msg)

                height = cleaned_data.get('height')
                if height is None:
                    self.add_error('height', msg)

                bcg_vaccine = cleaned_data.get('bcg_vaccine')
                bcg_vaccine_date = cleaned_data.get('bcg_vaccine_date')
                if bcg_vaccine and bcg_vaccine_date is None:
                    self.add_error('bcg_vaccine_date', msg)

                polio_vaccine = cleaned_data.get('polio_vaccine')
                polio_vaccine_date = cleaned_data.get('polio_vaccine_date')
                if polio_vaccine and polio_vaccine_date is None:
                    self.add_error('polio_vaccine_date', msg)

                dpt_vaccine = cleaned_data.get('dpt_vaccine')
                dpt_vaccine_date = cleaned_data.get('dpt_vaccine_date')
                if dpt_vaccine and dpt_vaccine_date is None:
                    self.add_error('dpt_vaccine_date', msg)

                hepatitis_b_vaccine = cleaned_data.get('hepatitis_b_vaccine')
                hepatitis_b_vaccine_date = cleaned_data.get('hepatitis_b_vaccine_date')
                if hepatitis_b_vaccine and hepatitis_b_vaccine_date is None:
                    self.add_error('hepatitis_b_vaccine_date', msg)

                flu_vaccine = cleaned_data.get('flu_vaccine')
                flu_vaccine_date = cleaned_data.get('flu_vaccine_date')
                if flu_vaccine and flu_vaccine_date is None:
                    self.add_error('flu_vaccine_date', msg)

                yellow_fever_vaccine = cleaned_data.get('yellow_fever_vaccine')
                yellow_fever_vaccine_date = cleaned_data.get('yellow_fever_vaccine_date')
                if yellow_fever_vaccine and yellow_fever_vaccine_date is None:
                    self.add_error('yellow_fever_vaccine_date', msg)

                spr_vaccine = cleaned_data.get('spr_vaccine')
                spr_vaccine_date = cleaned_data.get('spr_vaccine_date')
                if spr_vaccine and spr_vaccine_date is None:
                    self.add_error('spr_vaccine_date', msg)

                hpv_vaccine = cleaned_data.get('hpv_vaccine')
                hpv_vaccine_date = cleaned_data.get('hpv_vaccine_date')
                if hpv_vaccine and hpv_vaccine_date is None:
                    self.add_error('hpv_vaccine_date', msg)        
                
                pneumococcal_vaccine = cleaned_data.get('pneumococcal_vaccine')
                pneumococcal_vaccine_date = cleaned_data.get('pneumococcal_vaccine_date')
                if pneumococcal_vaccine and pneumococcal_vaccine_date is None:
                    self.add_error('pneumococcal_vaccine_date', msg)



