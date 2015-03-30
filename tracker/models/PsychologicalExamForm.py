# coding=utf-8

from PsychologicalExam import PsychologicalExam
from PsychologicalExam import PsychologicalExamDiagnosis
from django.db import models
from django.forms import ModelForm

class PsychologicalExamForm(ModelForm):
    class Meta:
        model = PsychologicalExam
        fields = (
            'date',
            'background_notes',
            'physical_description',
            'intelectual_notes',
            'organicity_notes',
            'psychomotor_notes',
            'emotional_notes',
            'recommendation',
        )
        labels = {
            'date': 'Fecha',
            'background_notes': 'Antecedents Patológicos Personales y Familiares Importantes',
            'physical_description': 'Descripción Fisica y Comportamiento',
            'intelectual_notes': 'Área Intelectual',
            'organicity_notes': 'Área Organicidad',
            'psychomotor_notes': 'Área Psciomotor',
            'emotional_notes': 'Área Afectiva Emocional',
            'recommendation': 'Recomendaciones',
        }

class PsychologicalExamDiagnosisForm(ModelForm):
    class Meta:
        model = PsychologicalExamDiagnosis
        fields = (
        )
        labels = {
            'diagnoses': 'Diagnostico',
            'diagnoses_cie_dsm9': 'CIE o DSM9',
        }

