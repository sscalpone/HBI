# coding=utf-8

import datetime

from django.contrib.auth.models import User
from django.db import models
from django.forms import ModelForm
from django.forms import RadioSelect

from Child import Child
from Signature import Signature

class MedicalExamPart2(models.Model):
    HIGH = 1
    MEDIUM = 2
    LOW = 3
    PRIORITY_CHOICES = (
        (HIGH, 'Alta Prioridad'),
        (MEDIUM, 'Prioridad Media'),
        (LOW, 'Prioridad Baja')
    )

    child = models.ForeignKey(Child)
    date = models.DateField()
    illness_notes = models.TextField(blank=True, null=True)
    appetite_notes = models.TextField(blank=True, null=True)
    sleep_notes = models.TextField(blank=True, null=True)
    blood_pressure = models.TextField(blank=True, null=True) #not in schema
    pulse = models.TextField(blank=True, null=True) #not in schema
    visual_acuity_left = models.TextField(blank=True, null=True)
    visual_acuity_right = models.TextField(blank=True, null=True)
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

    class Meta:
        app_label = 'tracker'
        db_table = 'tracker_medicalexampart2'


class MedicalExamPart2Form(ModelForm):
    class Meta:
        model = MedicalExamPart2
        fields = (
            'date',
            'illness_notes',
            'appetite_notes',
            'sleep_notes',
            'blood_pressure',
            'pulse',
            'visual_acuity_left',
            'visual_acuity_right',
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
            'illness_notes': 'Enfermedad Actual',
            'appetite_notes': 'Apetito',
            'sleep_notes': 'Sueño',
            'concerns_notes': 'Otras Problemas de Salud',
            'blood_pressure': 'Presión Arterial',
            'pulse': 'Pulso',
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

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(MedicalExamPart2Form, self).__init__(*args, **kwargs)

    def clean(self):
        msg = "Este campo es obligatorio."
        cleaned_data = super(MedicalExamPart2Form, self).clean()

        if self.request.method == 'POST':
            if 'submit' in self.request.POST:
                illness_notes = cleaned_data.get('illness_notes')
                if illness_notes=='':
                    self.add_error('illness_notes', msg)

                appetite_notes = cleaned_data.get('appetite_notes')
                if appetite_notes=='':
                    self.add_error('appetite_notes', msg)

                sleep_notes = cleaned_data.get('sleep_notes')
                if sleep_notes=='':
                    self.add_error('sleep_notes', msg)

                concerns_notes = cleaned_data.get('concerns_notes')
                if concerns_notes=='':
                    self.add_error('concerns_notes', msg)

                blood_pressure = cleaned_data.get('blood_pressure')
                if blood_pressure=='':
                    self.add_error('blood_pressure', msg)

                pulse = cleaned_data.get('pulse')
                if pulse=='':
                    self.add_error('pulse', msg)

                visual_acuity_left = cleaned_data.get('visual_acuity_left')
                if visual_acuity_left=='':
                    self.add_error('visual_acuity_left', msg)

                visual_acuity_right = cleaned_data.get('visual_acuity_right')
                if visual_acuity_right=='':
                    self.add_error('visual_acuity_right', msg)

                recommendations = cleaned_data.get('recommendations')
                if recommendations=='':
                    self.add_error('recommendations', msg)

                diagnosis = cleaned_data.get('diagnosis')
                if diagnosis=='':
                    self.add_error('diagnosis', msg)

                appearance_notes = cleaned_data.get('appearance_notes')
                if appearance_notes=='':
                    self.add_error('appearance_notes', msg) 
                
                skin_notes = cleaned_data.get('skin_notes')
                if skin_notes=='':
                    self.add_error('skin_mucosa_notes', msg) 
                
                lymph_notes = cleaned_data.get('TCSC_lymph_notes')
                if lymph_notes=='':
                    self.add_error('lymph_notes', msg) 

                neck_notes = cleaned_data.get('neck_notes')
                if neck_normal and neck_notes=='':
                    self.add_error('neck_notes', msg)

                lung_notes = cleaned_data.get('lung_notes')
                if lung_notes=='':
                    self.add_error('lung_notes', msg)

                cardio_notes = cleaned_data.get('cardio_notes')
                if cardio_notes=='':
                    self.add_error('cardio_notes', msg)

                abdomen_notes = cleaned_data.get('abdomen_notes')
                if abdomen_notes=='':
                    self.add_error('abdomen_notes', msg)

                genitourinary_notes = cleaned_data.get('genitourinary_notes')
                if genitourinary_notes=='':
                    self.add_error('genitourinary_notes', msg)

                extremities_notes = cleaned_data.get('extremities_notes')
                if extremities_notes=='':
                    self.add_error('extremities_notes', msg)

                neurological_notes = cleaned_data.get('neurological_notes')
                if neurological_notes=='':
                    self.add_error('neurological_notes', msg)

                treatment_notes = cleaned_data.get('treatment_notes')
                if treatment_notes=='':
                    self.add_error('treatment_notes', msg)

                recommendation = cleaned_data.get('recommendation')
                if recommendation=='':
                    self.add_error('recommendation', msg)

                diagnosis = cleaned_data('diagnosis')
                if diagnosis=='':
                    self.add_error('diagnosis', msg)




