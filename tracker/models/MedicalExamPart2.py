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
    concerns_notes = models.TextField(blank=True, null=True) #not in schema
    blood_pressure = models.TextField(blank=True, null=True) #not in schema
    pulse = models.TextField(blank=True, null=True) #not in schema
    visual_acuity_left = models.TextField(blank=True, null=True)
    visual_acuity_right = models.TextField(blank=True, null=True)
    appearance_normal = models.BooleanField(default=False) #not in schema
    appearance_notes = models.TextField(blank=True, null=True)
    skin_mucosa_normal = models.BooleanField(default=False) #not in schema
    skin_mucosa_notes = models.TextField(blank=True, null=True)
    TCSC_lymph_normal = models.BooleanField(default=False) #not in schema
    TCSC_lymph_notes = models.TextField(blank=True, null=True)
    head_neck_normal = models.BooleanField(default=False) #not in schema
    head_neck_notes = models.TextField(blank=True, null=True)
    thorax_lungs_normal = models.BooleanField(default=False) #not in schema
    thorax_lungs_notes = models.TextField(blank=True, null=True)
    cardio_normal = models.BooleanField(default=False) #not in schema
    cardio_notes = models.TextField(blank=True, null=True)
    abdomen_normal = models.BooleanField(default=False) #not in schema
    abdomen_notes = models.TextField(blank=True, null=True)
    genitourinary_normal = models.BooleanField(default=False) #not in schema
    genitourinary_notes = models.TextField(blank=True, null=True)
    extremities_normal = models.BooleanField(default=False) #not in schema
    extremities_notes = models.TextField(blank=True, null=True)
    neurological_normal = models.BooleanField(default=False) #not in schema
    neurological_notes = models.TextField(blank=True, null=True)
    diagnosis = models.TextField(blank=True, null=True)
    recommendations = models.TextField(blank=True, null=True)
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
            'concerns_notes',
            'blood_pressure',
            'pulse',
            'visual_acuity_left',
            'visual_acuity_right',
            'appearance_normal',
            'appearance_notes',
            'skin_mucosa_normal',
            'skin_mucosa_notes',
            'TCSC_lymph_normal',
            'TCSC_lymph_notes',
            'head_neck_normal',
            'head_neck_notes',
            'thorax_lungs_normal',
            'thorax_lungs_notes',
            'cardio_normal',
            'cardio_notes',
            'abdomen_normal',
            'abdomen_notes',
            'genitourinary_normal',
            'genitourinary_notes',
            'extremities_normal',
            'extremities_notes',
            'neurological_normal',
            'neurological_notes',
            'diagnosis',
            'recommendations',
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
            'appearance_normal': 'Aspecto General',
            'appearance_notes': 'Comentarios',
            'skin_mucosa_normal': 'Piel y Mucosas',
            'skin_mucosa_notes': 'Comentarios',
            'TCSC_lymph_normal': 'TCSC y G. Linfaticos',
            'TCSC_lymph_notes': 'Comentarios',
            'head_neck_normal': 'Cabeza y Cuello',
            'head_neck_notes': 'Comentarios',
            'thorax_lungs_normal': 'Tórax y Pulmones',
            'thorax_lungs_notes': 'Comentarios',
            'cardio_normal': 'Cardiovascular',
            'cardio_notes': 'Comentarios',
            'abdomen_normal': 'Abdomen',
            'abdomen_notes': 'Comentarios',
            'genitourinary_normal': 'Genitourinario y Ano',
            'genitourinary_notes': 'Comentarios',
            'extremities_normal': 'Extremidades',
            'extremities_notes': 'Comentarios',
            'neurological_normal': 'Neurological',
            'neurological_notes': 'Comentarios',
            'diagnosis': 'Diagnóstico',
            'recommendations': 'Otres Recomendaciones',
            'priority': 'Prioridad',
        }
        widgets = {
            'appearance_normal': RadioSelect(choices=((True, 'Anormal'),(False, 'Normal'))),
            'skin_mucosa_normal': RadioSelect(choices=((True, 'Anormal'),(False, 'Normal'))),
            'TCSC_lymph_normal': RadioSelect(choices=((True, 'Anormal'),(False, 'Normal'))),
            'head_neck_normal': RadioSelect(choices=((True, 'Anormal'),(False, 'Normal'))),
            'thorax_lungs_normal': RadioSelect(choices=((True, 'Anormal'),(False, 'Normal'))),
            'cardio_normal': RadioSelect(choices=((True, 'Anormal'),(False, 'Normal'))),
            'abdomen_normal': RadioSelect(choices=((True, 'Anormal'),(False, 'Normal'))),
            'genitourinary_normal': RadioSelect(choices=((True, 'Anormal'),(False, 'Normal'))),
            'extremities_normal': RadioSelect(choices=((True, 'Anormal'),(False, 'Normal'))),
            'neurological_normal': RadioSelect(choices=((True, 'Anormal'),(False, 'Normal'))),
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

                appearance_normal = cleaned_data.get('appearance_normal')
                appearance_notes = cleaned_data.get('appearance_notes')
                if appearance_normal and appearance_notes=='':
                    self.add_error('appearance_notes', msg) 
                
                skin_mucosa_normal = cleaned_data.get('skin_mucosa_normal')
                skin_mucosa_notes = cleaned_data.get('skin_mucosa_notes')
                if skin_mucosa_normal and skin_mucosa_notes=='':
                    self.add_error('skin_mucosa_notes', msg) 
                
                TCSC_lymph_normal = cleaned_data.get('TCSC_lymph_normal')
                TCSC_lymph_notes = cleaned_data.get('TCSC_lymph_notes')
                if TCSC_lymph_normal and TCSC_lymph_notes=='':
                    self.add_error('TCSC_lymph_notes', msg) 

                head_neck_normal = cleaned_data.get('head_neck_normal')
                head_neck_notes = cleaned_data.get('head_neck_notes')
                if head_neck_normal and head_neck_notes=='':
                    self.add_error('head_neck_notes', msg)

                thorax_lungs_normal = cleaned_data.get('thorax_lungs_normal')
                thorax_lungs_notes = cleaned_data.get('thorax_lungs_notes')
                if thorax_lungs_normal and thorax_lungs_notes=='':
                    self.add_error('thorax_lungs_notes', msg)

                cardio_normal = cleaned_data.get('cardio_normal')
                cardio_notes = cleaned_data.get('cardio_notes')
                if cardio_normal and cardio_notes=='':
                    self.add_error('cardio_notes', msg)

                abdomen_normal = cleaned_data.get('abdomen_normal')
                abdomen_notes = cleaned_data.get('abdomen_notes')
                if abdomen_normal and abdomen_notes=='':
                    self.add_error('abdomen_notes', msg)

                genitourinary_normal = cleaned_data.get('genitourinary_normal')
                genitourinary_notes = cleaned_data.get('genitourinary_notes')
                if genitourinary_normal and genitourinary_notes=='':
                    self.add_error('genitourinary_notes', msg)

                extremities_normal = cleaned_data.get('extremities_normal')
                extremities_notes = cleaned_data.get('extremities_notes')
                if extremities_normal and extremities_notes=='':
                    self.add_error('extremities_notes', msg)

                neurological_normal = cleaned_data.get('neurological_normal')
                neurological_notes = cleaned_data.get('neurological_notes')
                if neurological_normal and neurological_notes=='':
                    self.add_error('neurological_notes', msg)
