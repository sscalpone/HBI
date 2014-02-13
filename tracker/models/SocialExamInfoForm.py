# coding=utf-8

from tracker.models import SocialExamInfo
from django.forms import ModelForm
from django.forms import RadioSelect


class SocialExamInfoForm(ModelForm):
    class Meta:
        model = SocialExamInfo
        fields = (
            'date',
            'age_at_evaluation',
            'has_birth_certificate',
            'original_birth_certificate',
            'dni',
            'dni_in_process',
            'dni_comments',
            'sis',
            'sis_in_process',
            'sis_comments',
            'antecedents',
            'family_situation',
            'health_situation',
            'housing_situation',
            'economic_situation',
            'general_comments',
            'visitors_allowed',
            'visitors_notes',
            'social_diagnosis',
            'recommendation',
        )
        labels = {
            'date': "Fecha",
            'age_at_evaluation': "Edad",
            'has_birth_certificate': "Partida de Naciemiento",
            'original_birth_certificate': "Original",
            'dni': "DNI",
            'dni_in_process': "En proceso",
            'dni_comments': "Comentarios",
            'sis': "SIS",
            'sis_in_process': "En proceso",
            'sis_comments': "Comentarios",
            'antecedents': "Antecedentes",
            'family_situation': "Situacíon familiar",
            'health_situation': "Situacíon de salud",
            'housing_situation': "Situacíon de la vivienda",
            'economic_situation': "Situacíon económica",
            'general_comments': "Apreciaciones Generales del Niño/a",
            'visitors_allowed': "Recibe visitas",
            'visitors_notes': "Especificar",
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
