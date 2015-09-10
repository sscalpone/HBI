# coding=utf-8

import datetime

from django.db import models
from django.forms import ModelForm

from Child import Child
from Signature import Signature

class PsychologicalExam(models.Model):
    child = models.ForeignKey(Child)
    date = models.DateField()
    background_notes = models.TextField(null=True)
    physical_description = models.TextField(null=True)
    intelectual_notes = models.TextField(null=True)
    organicity_notes = models.TextField(null=True)
    psychomotor_notes = models.TextField(null=True)
    emotional_notes = models.TextField(null=True)
    recommendation = models.TextField(null=True)

    class Meta:
        app_label = 'tracker'
        db_table = 'tracker_psychologicalexam'

class PsychologicalExamDiagnosis(models.Model):
    exam = models.ForeignKey(PsychologicalExam)
    diagnoses = models.TextField()
    diagnoses_cie_dsm9 = models.TextField()

    class Meta:
        app_label = 'tracker'
        db_table = 'tracker_psychologicalexamdiagnosis'


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
