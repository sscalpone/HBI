# coding=utf-8

import datetime

from django.contrib.auth.models import User
from django.db import models
from django.forms import ModelForm
from django.forms import RadioSelect

from Child import Child
from Signature import Signature

class SocialExam(models.Model):
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
    antecedents = models.TextField(null=True)
    family_situation = models.TextField(null=True)
    health_situation = models.TextField(null=True)
    housing_situation = models.TextField(null=True)
    economic_situation = models.TextField(null=True)
    general_comments = models.TextField(null=True)
    visitors_allowed = models.BooleanField(default=True)
    visitors_allowed_no_comments = models.TextField(blank=True, null=True)
    social_diagnosis = models.TextField(null=True)
    recommendation = models.TextField(null=True)

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
