# coding=utf-8

import datetime

from django.contrib.auth.models import User
from django.db import models
from django.forms import ModelForm
from django.forms import RadioSelect

from Child import Child
from Signature import Signature

class SocialExam(models.Model):
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
    has_birth_certificate = models.BooleanField(default=False)
    original_birth_certificate = models.BooleanField(default=False)
    dni = models.BooleanField(default=False)
    dni_in_process = models.BooleanField(default=False)
    dni_no_comments = models.TextField(blank=True, null=True)
    sis = models.BooleanField(default=False)
    sis_in_process = models.BooleanField(default=False)
    sis_no_comments = models.TextField(blank=True, null=True)
    antecedents = models.TextField(blank=True, null=True)
    family_situation = models.TextField(blank=True, null=True)
    health_situation = models.TextField(blank=True, null=True)
    housing_situation = models.TextField(blank=True, null=True)
    economic_situation = models.TextField(blank=True, null=True)
    general_comments = models.TextField(blank=True, null=True)
    visitors_allowed = models.BooleanField(default=True)
    visitors_allowed_no_comments = models.TextField(blank=True, null=True)
    social_diagnosis = models.TextField(blank=True, null=True)
    recommendation = models.TextField(blank=True, null=True)
    priority = models.IntegerField(choices=PRIORITY_CHOICES, 
                                   default=HIGH)
    signature = models.ForeignKey(Signature, blank=True, null=True)

    class Meta:
        app_label = 'tracker'
        db_table = 'tracker_socialexam'


class SocialExamForm(ModelForm):
    class Meta:
        model = SocialExam
        fields = (
            'date',
            'has_birth_certificate',
            'original_birth_certificate',
            'dni',
            'dni_in_process',
            'dni_no_comments',
            'sis',
            'sis_in_process',
            'sis_no_comments',
            'antecedents',
            'family_situation',
            'health_situation',
            'housing_situation',
            'economic_situation',
            'general_comments',
            'visitors_allowed',
            'visitors_allowed_no_comments',
            'social_diagnosis',
            'recommendation',
            'priority'
        )
        labels = {
            'date': "Fecha",
            'has_birth_certificate': "Partida de Nacimiento",
            'original_birth_certificate': "Original",
            'dni': "DNI",
            'dni_in_process': "En El Proceso",
            'dni_no_comments': "Comentarios",
            'sis': "SIS",
            'sis_in_process': "En El Proceso",
            'sis_no_comments': "Comentarios",
            'antecedents': "Antecedents",
            'family_situation': "Situación Familiar",
            'health_situation': "Situación de Salud",
            'housing_situation': "Situación de la Vivienda",
            'economic_situation': "Situación Económica",
            'general_comments': "Apreciaciones Generales del Niño/a",
            'visitors_allowed': "Recibe Visitas",
            'visitors_allowed_no_comments': "Comentarios",
            'social_diagnosis': "Diagnostico Social",
            'recommendation': "Recomendaciones",
            'priority': 'Prioridad',
        }
        widgets = {
            'has_birth_certificate': RadioSelect(choices=((True, 'Sí'),(False, 'No'))),
            'original_birth_certificate': RadioSelect(choices=((True, 'Sí'),(False, 'No'))),
            'dni': RadioSelect(choices=((True, 'Sí'),(False, 'No'))),
            'dni_in_process': RadioSelect(choices=((True, 'Sí'),(False, 'No'))),
            'sis': RadioSelect(choices=((True, 'Sí'),(False, 'No'))),
            'sis_in_process': RadioSelect(choices=((True, 'Sí'),(False, 'No'))),
            'visitors_allowed': RadioSelect(choices=((True, 'Sí'),(False, 'No'))),
        }

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(SocialExamForm, self).__init__(*args, **kwargs)

    def clean(self):
        msg = "Este campo es obligatorio."
        cleaned_data = super(SocialExamForm, self).clean()
        
        if self.request.method=='POST':
            
            if 'submit' in self.request.POST:
                dni = cleaned_data.get('dni')
                dni_no_comments = cleaned_data.get('dni_no_comments')
                if not dni and dni_no_comments=='':
                    self.add_error('dni_no_comments', msg)
                
                sis = cleaned_data.get('sis')
                sis_no_comments = cleaned_data.get('sis_no_comments')
                if not sis and sis_no_comments=='':
                    self.add_error('sis_no_comments', msg)
                
                antecedents = cleaned_data.get('antecedents')
                if antecedents=='':
                    self.add_error('antecedents', msg)
                
                family_situation = cleaned_data.get('family_situation')
                if family_situation=='':
                    self.add_error('family_situation', msg)
                
                health_situation = cleaned_data.get('health_situation')
                if health_situation=='':
                    self.add_error('health_situation', msg)
                
                economic_situation = cleaned_data.get('economic_situation')
                if economic_situation=='':
                    self.add_error('economic_situation', msg)
                
                general_comments = cleaned_data.get('general_comments')
                if general_comments=='':
                    self.add_error('general_comments', msg)
                
                housing_situation = cleaned_data.get('housing_situation')
                if housing_situation=='':
                    self.add_error('housing_situation', msg)
                
                visitors_allowed = cleaned_data.get('visitors_allowed')
                visitors_allowed_no_comments = cleaned_data.get('visitors_allowed_no_comments')
                if not visitors_allowed and visitors_allowed_no_comments=='':
                    self.add_error('visitors_allowed_no_comments', msg)
                
                social_diagnosis = cleaned_data.get('social_diagnosis')
                if social_diagnosis=='':
                    self.add_error('social_diagnosis', msg)
                
                recommendation = cleaned_data.get('recommendation')
                if recommendation=='':
                    self.add_error('recommendation', msg)








