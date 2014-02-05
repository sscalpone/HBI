# coding=utf-8

import datetime
from PsychologicalExamInfo import PsychologicalExamInfo
from django.db import models
from django.forms import ModelForm

class PsychologicalExamInfoForm(ModelForm):
    class Meta:
        model = PsychologicalExamInfo
        fields = '__all__'
        labels = {
            'date': 'Fecha',
            'family_notes': 'Antecedentes Patologicos Personales y familiares importantes',
            'physical_description': 'Descripcion fisica y comportamiento',
# Analisis e interpretacion de los resultados obtenidas
            'intelectual_notes': 'Área Intelectual',
            'organicity_notes': 'Área organicidad',
            'psychomotor_notes': 'Área psicomotora',
            'recommendation': 'Recomendaciones',
        }

# diagnóstico

