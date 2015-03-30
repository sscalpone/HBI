# coding=utf-8

from MedicalExamPart2 import MedicalExamPart2
from django.db import models
from django.forms import ModelForm

class MedicalExamPart2Form(ModelForm):
    class Meta:
        model = MedicalExamPart2
        fields = (
            'date',
            'appetite_notes',
            'sleep_notes',
            'concerns_notes',
            'blood_pressure',
            'pulse',
            'visual_acuity_left',
            'visual_acuity_right',
            'appearance_normal',
            'skin_mucosa_normal',
            'TCSC_lymph_normal',
            'head_neck_normal',
            'thorax_lungs_normal',
            'cardio_normal',
            'abdomen_normal',
            'genitourinary_normal',
            'extremities_normal',
            'neurological_normal',
            'recommendations',
        )
        labels = {
            'date': 'Fecha',
            'appetite_notes': 'Apetito',
            'sleep_notes': 'Sueño',
            'concerns_notes': 'Otras Problemas de Salud',
            'blood_pressure': 'Presión Arterial',
            'pulse': 'Pulso',
            'visual_acuity_left': 'Agudeza Visual Izquierdo',
            'visual_acuity_right': 'Agudeza Visual Derecha',
            'appearance_normal': 'Aspecto General Normal/Anormal',
            'skin_mucosa_normal': 'Piel y Mucosas Normal/Anormal',
            'TCSC_lymph_normal': 'TCSC y G. Linfaticos Normal/Anormal',
            'head_neck_normal': 'Cabeza y Cuello Normal/Anormal',
            'thorax_lungs_normal': 'Tórax y Pulmones  Normal/Anormal',
            'cardio_normal': 'Cardiovascular  Normal/Anormal',
            'abdomen_normal': 'Abdomen Normal/Anormal',
            'genitourinary_normal': 'Genitourinario y Ano   Normal/Anormal',
            'extremities_normal': 'Extremidades  Normal/Anormal',
            'neurological_normal': 'Neurological Normal/Anormal',
            'recommendations': 'Otres Recomendaciones',
        }
