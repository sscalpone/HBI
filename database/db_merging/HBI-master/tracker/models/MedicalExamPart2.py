# coding=utf-8

import datetime

from django.contrib.auth.models import User
from django.db import models
from django.forms import ModelForm
from django.forms import RadioSelect

from Child import Child
from Signature import Signature


"""The model for Medical Exam Part 2 stores the second half the 
medical exam, primarily observations on the child's physical and 
mental health. Also notes any treatment plans. It references the Child 
model and the Signature model. It affects priority. All fields are 
allowed to be saved null so that forms can be saved before validation 
to prevent losing information if the form can't be completed. This is 
overriden in the clean() method.
"""
class MedicalExamPart2(models.Model):
    # Priority choices
    HIGH = 1
    MEDIUM = 2
    LOW = 3
    PRIORITY_CHOICES = (
        (HIGH, 'Alta Prioridad'),
        (MEDIUM, 'Prioridad Media'),
        (LOW, 'Prioridad Baja')
    )
    
    uuid = models.CharField(max_length=200, primary_key=True)
    child = models.ForeignKey(Child)
    date = models.DateField()
    appetite_notes = models.TextField(blank=True, null=True)
    sleep_notes = models.TextField(blank=True, null=True)
    bowel_notes = models.TextField(blank=True, null=True)
    appearance_notes = models.TextField(blank=True, null=True)
    skin_notes = models.TextField(blank=True, null=True)
    lymph_notes = models.TextField(blank=True, null=True)
    neck_notes = models.TextField(blank=True, null=True)
    lung_notes = models.TextField(blank=True, null=True)
    cardio_notes = models.TextField(blank=True, null=True)
    abdomen_notes = models.TextField(blank=True, null=True)
    genitourinary_notes = models.TextField(blank=True, null=True)
    extremities_notes = models.TextField(blank=True, null=True)
    neurological_notes = models.TextField(blank=True, null=True)
    treatment_notes = models.TextField(blank=True, null=True)
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
        db_table = 'tracker_medicalexampart2'
        default_permissions = ()


"""Form for the Mecical Exam Part 2 model."""
class MedicalExamPart2Form(ModelForm):

    # Meta class defines the fields and Spanish labels for the form.
    class Meta:
        model = MedicalExamPart2
        
        fields = (
            'date',
            'appetite_notes',
            'sleep_notes',
            'bowel_notes',
            'appearance_notes',
            'skin_notes',
            'lymph_notes',
            'neck_notes',
            'lung_notes',
            'cardio_notes',
            'abdomen_notes',
            'genitourinary_notes',
            'extremities_notes',
            'neurological_notes',
            'treatment_notes',
            'diagnosis',
            'recommendation',
            'priority',
        )
        
        labels = {
            'date': 'Fecha',
            'appetite_notes': 'Apetito',
            'sleep_notes': 'Sueño',
            'bowel_notes': 'Deposiciones',
            'visual_acuity_left': 'Agudeza Visual Izquierdo',
            'visual_acuity_right': 'Agudeza Visual Derecha',
            'appearance_notes': 'Comentarios',
            'skin_notes': 'Comentarios de Piel',
            'lymph_notes': 'Ganglios Comentarios',
            'neck_notes': 'Comentarios del Cuello',
            'lung_notes': 'Comentarios Pulmones',
            'cardio_notes': 'Comentarios Cardiovasculares',
            'abdomen_notes': 'Comentarios Abdomen',
            'genitourinary_notes': 'Comentarios Genitourinarias',
            'extremities_notes': 'Extremidades Comentarios',
            'neurological_notes': 'Neurológicos Comentarios',
            'treatment_notes': 'Tratamiento Comentarios',
            'diagnosis': 'Diagnóstico',
            'recommendation': 'Recomendaciones',
            'priority': 'Prioridad',
        }

    # Override __init__ so 'request' can be accessed in the clean() 
    # function.
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(MedicalExamPart2Form, self).__init__(*args, **kwargs)

    # Override clean so forms can be saved without validating (so data 
    # isn't lost if the form can't be completed), but still raises 
    # exceptions when form is done incorrectly.
    def clean(self):
        msg = "Este campo es obligatorio."
        cleaned_data = super(MedicalExamPart2Form, self).clean()

        # On validation ('submit' in request), checks if signature 
        # forms fields are filled out and raises exceptions on any 
        # fields left blank.
        if (self.request.POST):
            if ('submit' in self.request.POST):
                appetite_notes = cleaned_data.get('appetite_notes')
                if (appetite_notes == ''):
                    self.add_error('appetite_notes', msg)

                sleep_notes = cleaned_data.get('sleep_notes')
                if (sleep_notes == ''):
                    self.add_error('sleep_notes', msg)

                bowel_notes = cleaned_data.get('bowel_notes')
                if (bowel_notes == ''):
                    self.add_error('bowel_notes', msg)

                appearance_notes = cleaned_data.get('appearance_notes')
                if (appearance_notes == ''):
                    self.add_error('appearance_notes', msg) 
                
                skin_notes = cleaned_data.get('skin_notes')
                if (skin_notes == ''):
                    self.add_error('skin_mucosa_notes', msg) 
                
                lymph_notes = cleaned_data.get('TCSC_lymph_notes')
                if (lymph_notes == ''):
                    self.add_error('lymph_notes', msg) 

                neck_notes = cleaned_data.get('neck_notes')
                if (neck_notes == ''):
                    self.add_error('neck_notes', msg)

                lung_notes = cleaned_data.get('lung_notes')
                if (lung_notes == ''):
                    self.add_error('lung_notes', msg)

                cardio_notes = cleaned_data.get('cardio_notes')
                if (cardio_notes == ''):
                    self.add_error('cardio_notes', msg)

                abdomen_notes = cleaned_data.get('abdomen_notes')
                if (abdomen_notes == ''):
                    self.add_error('abdomen_notes', msg)

                genitourinary_notes = cleaned_data.get('genitourinary_notes')
                if (genitourinary_notes == ''):
                    self.add_error('genitourinary_notes', msg)

                extremities_notes = cleaned_data.get('extremities_notes')
                if (extremities_notes == ''):
                    self.add_error('extremities_notes', msg)

                neurological_notes = cleaned_data.get('neurological_notes')
                if (neurological_notes == ''):
                    self.add_error('neurological_notes', msg)

                treatment_notes = cleaned_data.get('treatment_notes')
                if (treatment_notes == ''):
                    self.add_error('treatment_notes', msg)

                recommendation = cleaned_data.get('recommendation')
                if (recommendation == ''):
                    self.add_error('recommendation', msg)

                diagnosis = cleaned_data('diagnosis')
                if (diagnosis == ''):
                    self.add_error('diagnosis', msg)




