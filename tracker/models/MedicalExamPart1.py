# coding=utf-8

import datetime
import uuid

from django.contrib.auth.models import User
from django.db import models
from django.forms import ModelForm
from django.forms import RadioSelect

from Child import Child
from Signature import Signature


"""The Medical Exam Part 1 model stores the first part of the child's 
medical exam; mainly vaccine administration dates, as well as height, 
weight, and hemoglobin. It references the Child model and the 
Signature model. It affects priority. All fields are allowed to be 
saved null so that forms can be saved before validation to prevent 
losing information if the form can't be completed. This is overriden 
in the clean() method.
"""
class MedicalExamPart1(models.Model):
    # Priority choices
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
    diagnosis = models.TextField(blank=True, null=True)
    recommendation = models.TextField(blank=True, null=True)
    priority = models.IntegerField(choices=PRIORITY_CHOICES, 
                                   default=HIGH)
    signature = models.ForeignKey(Signature, blank=True, null=True)
    # For de-duping forms that have been edited.
    last_saved = models.DateTimeField(blank=True, null=True) 

    # Meta class defines database table and labels, and clears any 
    # default permissions.
    class Meta:
        app_label = 'tracker'
        db_table = 'tracker_medicalexampart1'
        default_permissions = ()


"""Growth model stores information from the Medical Exam Part 1 and 
Child models to generate the growth graph displayed on the medical 
exam part 1 page.
"""
class Growth(models.Model):
    child = models.ForeignKey(Child)
    uuid = models.CharField(max_length=200, unique=True, default=uuid.uuid4)
    exam = models.ForeignKey(MedicalExamPart1)
    date = models.DateField()
    height = models.FloatField(blank=True, null=True)
    weight = models.FloatField(blank=True, null=True)
    age = models.FloatField(blank=True, null=True)
    gender = models.CharField(max_length=6, blank=True, null=True)

    # Meta class defines database table and labels, and clears any 
    # default permissions.
    class Meta:
        app_label = 'tracker'
        db_table = 'tracker_growth'
        default_permissions = ()


"""The form the Medical Exam Part 1 model."""
class MedicalExamPart1Form(ModelForm):

    # Meta class defines the fields and Spanish labels for the form.
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
            'diagnosis',
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
            'polio_vaccine_date': 'Antipoliomielitica Fecha de ' 
                'Administracion',
            'dpt_vaccine_date': 'DPT Fecha de Administracion',
            'hepatitis_b_vaccine_date': 'Hepatitis B Fecha de Administracion',
            'flu_vaccine_date': 'Hemofilus Influenza Fecha de Administracion',
            'yellow_fever_vaccine_date': 'Fiebre Amarilla Fecha de '
                'Administracion',
            'spr_vaccine_date': 'SPR Fecha de Administracion',
            'hpv_vaccine_date': 'HPV Fecha de Administracion',
            'pneumococcal_vaccine_date': 'Neumococo Fecha de Administracion',
            'diagnosis': 'Diagnóstico',
            'recommendation': 'Recomendaciones',
            'priority': 'Prioridad',
        }

    # Override __init__ so 'request' can be accessed in the clean() 
    # function.
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(MedicalExamPart1Form, self).__init__(*args, **kwargs)

    # Override clean so forms can be saved without validating (so data 
    # isn't lost if the form can't be completed), but still raises 
    # exceptions when form is done incorrectly.
    def clean(self):
        msg = "Este campo es obligatorio."
        cleaned_data = super(MedicalExamPart1Form, self).clean()

        # On validation ('submit' in request), checks if signature 
        # forms fields are filled out and raises exceptions on any 
        # fields left blank.
        if (self.request.POST):
            if ('submit' in self.request.POST):
                weight = cleaned_data.get('weight')
                if (weight is None):
                    self.add_error('weight', msg)

                height = cleaned_data.get('height')
                if (height is None):
                    self.add_error('height', msg)

                visual_acuity_left = cleaned_data.get('visual_acuity_left')
                if (visual_acuity_left == ''):
                    self.add_error('visual_acuity_left', msg)

                visual_acuity_right = cleaned_data.get('visual_acuity_right')
                if (visual_acuity_right == ''):
                    self.add_error('visual_acuity_right', msg)

                diagnosis = cleaned_data('diagnosis')
                if (diagnosis == ''):
                    self.add_error('diagnosis', msg)

                recommendation = cleaned_data.get('recommendation')
                if (recommendation == ''):
                    self.add_error('recommendation', msg)

                # Checks that there are notes on child's hemoglobin if 
                # hemoglobin is marked abnormal.
                hemoglobin_abnormal = cleaned_data.get('hemoglobin_abnormal')
                hemoglobin_notes = cleaned_data.get('hemoglobin_notes')
                if (hemoglobin_abnormal and hemoglobin_notes == ''):
                    self.add_error('hemoglobin_notes', msg)
