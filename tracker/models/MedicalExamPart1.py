# coding=utf-8

import datetime
import uuid

from django.contrib.auth.models import User
from django.db import models
from django.forms import ModelForm
from django.forms import RadioSelect

from Child import Child
from Signature import Signature


class MedicalExamPart1(models.Model):
    HIGH = 1
    MEDIUM = 2
    LOW = 3
    PRIORITY_CHOICES = (
        (HIGH, 'Alta Prioridad'),
        (MEDIUM, 'Prioridad Media'),
        (LOW, 'Prioridad Baja')
    )

    uuid = models.CharField(max_length=200, unique=True, default=uuid.uuid4)
    child = models.ForeignKey(Child)
    date = models.DateField()
    height = models.FloatField(blank=True, null=True)
    weight = models.FloatField(blank=True, null=True)
    hemoglobin_abnormal = models.BooleanField(default=False)
    hemoglobin_notes = models.TextField(blank=True, null=True)
    visual_acuity_left = models.TextField(blank=True, null=True)
    visual_acuity_right = models.TextField(blank=True, null=True)
    bcg_vaccine_date = models.DateField(blank=True, null=True)
    polio_vaccine_date = models.DateField(blank=True, null=True)
    dpt_vaccine_date = models.DateField(blank=True, null=True)
    hepatitis_b_vaccine_date = models.DateField(blank=True, null=True)
    flu_vaccine_date = models.DateField(blank=True, null=True)
    yellow_fever_vaccine_date = models.DateField(blank=True, null=True)
    spr_vaccine_date = models.DateField(blank=True, null=True)
    hpv_vaccine_date = models.DateField(blank=True, null=True)
    pneumococcal_vaccine_date = models.DateField(blank=True, null=True)
    recommendation = models.TextField(blank=True, null=True)
    priority = models.IntegerField(choices=PRIORITY_CHOICES, 
                                   default=HIGH)
    signature = models.ForeignKey(Signature, blank=True, null=True)
    last_saved = models.DateTimeField()

    class Meta:
        app_label = 'tracker'
        db_table = 'tracker_medicalexampart1'
        default_permissions = ()

class Growth(models.Model):
    child = models.ForeignKey(Child)
    exam = models.ForeignKey(MedicalExamPart1)
    date = models.DateField()
    height = models.FloatField(blank=True, null=True)
    weight = models.FloatField(blank=True, null=True)
    age = models.FloatField(blank=True, null=True)
    gender = models.CharField(max_length=6, blank=True, null=True)

    class Meta:
        app_label = 'tracker'
        db_table = 'tracker_growth'
        default_permissions = ()


class MedicalExamPart1Form(ModelForm):
    class Meta:
        model = MedicalExamPart1
        fields = (
            'date',
            'height',
            'weight',
            'hemoglobin_abnormal',
            'hemoglobin_notes',
            'visual_acuity_left',
            'visual_acuity_right',
            'bcg_vaccine_date',
            'polio_vaccine_date',
            'dpt_vaccine_date',
            'hepatitis_b_vaccine_date',
            'flu_vaccine_date',
            'yellow_fever_vaccine_date',
            'spr_vaccine_date',
            'hpv_vaccine_date',
            'pneumococcal_vaccine_date',
            'recommendation',
            'priority',
        )
        labels = {
            'date': 'Fecha',
            'height': 'Estatura (cm)',
            'weight': 'Peso (kg)',
            'hemoglobin_abnormal': 'Hemoglobina',
            'hemoglobin_notes': 'Comentarios',
            'visual_acuity_left': 'Agudeza Visual Izquierdo',
            'visual_acuity_right': 'Agudeza Visual Derecha',
            'bcg_vaccine_date': 'BCG Fecha de Administracion',
            'polio_vaccine_date': 'Antipoliomielitica Fecha de Administracion',
            'dpt_vaccine_date': 'DPT Fecha de Administracion',
            'hepatitis_b_vaccine_date': 'Hepatitis B Fecha de Administracion',
            'flu_vaccine_date': 'Hemofilus Influenza Fecha de Administracion',
            'yellow_fever_vaccine_date': 'Fiebre Amarilla Fecha de Administracion',
            'spr_vaccine_date': 'SPR Fecha de Administracion',
            'hpv_vaccine_date': 'HPV Fecha de Administracion',
            'pneumococcal_vaccine_date': 'Neumococo Fecha de Administracion',
            'recommendation': 'Recomendaciones',
            'priority': 'Prioridad',
        }


    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(MedicalExamPart1Form, self).__init__(*args, **kwargs)

    def clean(self):
        msg = "Este campo es obligatorio."
        cleaned_data = super(MedicalExamPart1Form, self).clean()

        if self.request.POST:
            if 'submit' in self.request.POST:

                hemoglobin_abnormal = cleaned_data.get('hemoglobin_abnormal')
                hemoglobin_notes = cleaned_data.get('hemoglobin_notes')
                if hemoglobin_abnormal and hemoglobin_notes=='':
                    self.add_error('hemoglobin_notes', msg)

                weight = cleaned_data.get('weight')
                if weight is None:
                    self.add_error('weight', msg)

                height = cleaned_data.get('height')
                if height is None:
                    self.add_error('height', msg)

                visual_acuity_left = cleaned_data.get('visual_acuity_left')
                if visual_acuity_left=='':
                    self.add_error('visual_acuity_left', msg)

                # visual_acuity_right = cleaned_data.get('visual_acuity_right')
                # if visual_acuity_right=='':
                #     self.add_error('visual_acuity_right', msg)

                # bcg_vaccine = cleaned_data.get('bcg_vaccine')
                # bcg_vaccine_date = cleaned_data.get('bcg_vaccine_date')
                # if bcg_vaccine and bcg_vaccine_date is None:
                #     self.add_error('bcg_vaccine_date', msg)

                # polio_vaccine = cleaned_data.get('polio_vaccine')
                # polio_vaccine_date = cleaned_data.get('polio_vaccine_date')
                # if polio_vaccine and polio_vaccine_date is None:
                #     self.add_error('polio_vaccine_date', msg)

                # dpt_vaccine = cleaned_data.get('dpt_vaccine')
                # dpt_vaccine_date = cleaned_data.get('dpt_vaccine_date')
                # if dpt_vaccine and dpt_vaccine_date is None:
                #     self.add_error('dpt_vaccine_date', msg)

                # hepatitis_b_vaccine = cleaned_data.get('hepatitis_b_vaccine')
                # hepatitis_b_vaccine_date = cleaned_data.get('hepatitis_b_vaccine_date')
                # if hepatitis_b_vaccine and hepatitis_b_vaccine_date is None:
                #     self.add_error('hepatitis_b_vaccine_date', msg)

                # flu_vaccine = cleaned_data.get('flu_vaccine')
                # flu_vaccine_date = cleaned_data.get('flu_vaccine_date')
                # if flu_vaccine and flu_vaccine_date is None:
                #     self.add_error('flu_vaccine_date', msg)

                # yellow_fever_vaccine = cleaned_data.get('yellow_fever_vaccine')
                # yellow_fever_vaccine_date = cleaned_data.get('yellow_fever_vaccine_date')
                # if yellow_fever_vaccine and yellow_fever_vaccine_date is None:
                #     self.add_error('yellow_fever_vaccine_date', msg)

                # spr_vaccine = cleaned_data.get('spr_vaccine')
                # spr_vaccine_date = cleaned_data.get('spr_vaccine_date')
                # if spr_vaccine and spr_vaccine_date is None:
                #     self.add_error('spr_vaccine_date', msg)

                # hpv_vaccine = cleaned_data.get('hpv_vaccine')
                # hpv_vaccine_date = cleaned_data.get('hpv_vaccine_date')
                # if hpv_vaccine and hpv_vaccine_date is None:
                #     self.add_error('hpv_vaccine_date', msg)        
                
                # pneumococcal_vaccine = cleaned_data.get('pneumococcal_vaccine')
                # pneumococcal_vaccine_date = cleaned_data.get('pneumococcal_vaccine_date')
                # if pneumococcal_vaccine and pneumococcal_vaccine_date is None:
                #     self.add_error('pneumococcal_vaccine_date', msg)

                recommendation = cleaned_data.get('recommendation')
                if recommendation=='':
                    self.add_error('recommendation', msg)



