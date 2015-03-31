# coding=utf-8

from MedicalExamPart2 import MedicalExamPart2
from django.db import models
from django.forms import ModelForm
from django.forms import RadioSelect

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
            'recommendations',
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
            'recommendations': 'Otres Recomendaciones',
        }
        widgets = {
            'appearance_normal': RadioSelect(choices=((True, 'Normal'),(False, 'Anormal'))),
            'skin_mucosa_normal': RadioSelect(choices=((True, 'Normal'),(False, 'Anormal'))),
            'TCSC_lymph_normal': RadioSelect(choices=((True, 'Normal'),(False, 'Anormal'))),
            'head_neck_normal': RadioSelect(choices=((True, 'Normal'),(False, 'Anormal'))),
            'thorax_lungs_normal': RadioSelect(choices=((True, 'Normal'),(False, 'Anormal'))),
            'cardio_normal': RadioSelect(choices=((True, 'Normal'),(False, 'Anormal'))),
            'abdomen_normal': RadioSelect(choices=((True, 'Normal'),(False, 'Anormal'))),
            'genitourinary_normal': RadioSelect(choices=((True, 'Normal'),(False, 'Anormal'))),
            'extremities_normal': RadioSelect(choices=((True, 'Normal'),(False, 'Anormal'))),
            'neurological_normal': RadioSelect(choices=((True, 'Normal'),(False, 'Anormal'))),
        }

