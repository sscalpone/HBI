# coding=utf-8

import datetime

from django.db import models
from django.forms import ModelForm

from Child import Child
from Signature import Signature


class PsychologicalExam(models.Model):
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
    background_notes = models.TextField(blank=True, null=True)
    physical_description = models.TextField(blank=True, null=True)
    intellectual_notes = models.TextField(blank=True, null=True)
    organicity_notes = models.TextField(blank=True, null=True)
    psychomotor_notes = models.TextField(blank=True, null=True)
    emotional_notes = models.TextField(blank=True, null=True)
    diagnosis = models.TextField(blank=True, null=True)
    recommendation = models.TextField(blank=True, null=True)
    priority = models.IntegerField(choices=PRIORITY_CHOICES, 
                                   default=HIGH)
    signature = models.ForeignKey(Signature, blank=True, null=True)

    class Meta:
        app_label = 'tracker'
        db_table = 'tracker_psychologicalexam'


class PsychologicalExamForm(ModelForm):
    class Meta:
        model = PsychologicalExam
        fields = (
            'date',
            'background_notes',
            'physical_description',
            'intellectual_notes',
            'organicity_notes',
            'psychomotor_notes',
            'emotional_notes',
            'diagnosis',
            'recommendation',
            'priority'
        )
        labels = {
            'date': 'Fecha',
            'background_notes': 'Antecedents Patológicos Personales y Familiares Importantes',
            'physical_description': 'Descripción Fisica y Comportamiento',
            'intellectual_notes': 'Área Intelectual',
            'organicity_notes': 'Área Organicidad',
            'psychomotor_notes': 'Área Psciomotor',
            'emotional_notes': 'Área Afectiva Emocional',
            'diagnosis': 'Diagnóstico',
            'recommendation': 'Recomendaciones',
            'priority': 'Prioridad',
        }

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(PsychologicalExamForm, self).__init__(*args, **kwargs)

    def clean(self):
        msg = "Este campo es obligatorio."
        cleaned_data = super(PsychologicalExamForm, self).clean()
        if self.request.method=='POST':
            if 'submit' in self.request.POST:
                background_notes = cleaned_data.get('background_notes')
                if background_notes=='':
                    self.add_error('background_notes', msg)
                physical_description = cleaned_data.get('physical_description')
                if physical_description=='':
                    self.add_error('physical_description', msg)
                intellectual_notes = cleaned_data.get('intellectual_notes')
                if intellectual_notes=='':
                    self.add_error('intellectual_notes', msg)
                organicity_notes = cleaned_data.get('organicity_notes')
                if organicity_notes=='':
                    self.add_error('organicity_notes', msg)
                psychomotor_notes = cleaned_data.get('psychomotor_notes')
                if psychomotor_notes=='':
                    self.add_error('psychomotor_notes', msg)
                emotional_notes = cleaned_data.get('emotional_notes')
                if emotional_notes=='':
                    self.add_error('emotional_notes', msg)
                diagnosis = cleaned_data.get('diagnosis')
                if diagnosis=='':
                    self.add_error('diagnosis', msg)
                recommendation = cleaned_data.get('recommendation')
                if recommendation=='':
                    self.add_error('recommendation', msg)

