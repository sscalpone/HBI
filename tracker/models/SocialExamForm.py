# coding=utf-8

from tracker.models import SocialExam
from django.forms import ModelForm
from django.forms import RadioSelect

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
            'has_birth_certificate': RadioSelect(choices=((True, 'Si'),(False, 'No'))),
            'original_birth_certificate': RadioSelect(choices=((True, 'Si'),(False, 'No'))),
            'dni': RadioSelect(choices=((True, 'Si'),(False, 'No'))),
            'dni_in_process': RadioSelect(choices=((True, 'Si'),(False, 'No'))),
            'sis': RadioSelect(choices=((True, 'Si'),(False, 'No'))),
            'sis_in_process': RadioSelect(choices=((True, 'Si'),(False, 'No'))),
            'visitors_allowed': RadioSelect(choices=((True, 'Si'),(False, 'No'))),
        }
