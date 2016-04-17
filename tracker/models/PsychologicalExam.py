# coding=utf-8

import datetime
import uuid

from django.db import models
from django.forms import ModelForm
from django.forms import DateInput

from Child import Child


"""The PsychologicalExam model stores information about each child's 
psychological health. It references the Child model and the Signature 
model. It affects priority. All fields are allowed to be saved null so 
that forms can be saved before validation to prevent losing 
information if the form can't be completed. This is overriden in the 
clean() method.
"""
class PsychologicalExam(models.Model):
    # Priority choices
    HIGH = 1
    MEDIUM = 2
    LOW = 3
    PRIORITY_CHOICES = (
        (HIGH, 'Alta Prioridad'),
        (MEDIUM, 'Prioridad Media'),
        (LOW, 'Prioridad Baja')
    )

    # Fields
    uuid = models.CharField(max_length=200, unique=True, default=uuid.uuid4)
    child = models.ForeignKey(Child, blank=True, null=True)
    date = models.DateField(default=datetime.date.today)
    family_notes = models.TextField(blank=True, null=True)
    physical_description = models.TextField(blank=True, null=True)
    intellectual_notes = models.TextField(blank=True, null=True)
    organicity_notes = models.TextField(blank=True, null=True)
    psychomotor_notes = models.TextField(blank=True, null=True)
    emotional_notes = models.TextField(blank=True, null=True)
    diagnosis = models.TextField(blank=True, null=True)
    recommendation = models.TextField(blank=True, null=True)
    priority = models.IntegerField(choices=PRIORITY_CHOICES, 
                                   default=HIGH)
    signature_name = models.CharField(max_length=200, blank=True, null=True)
    signature_surname = models.CharField(max_length=200, blank=True, null=True)
    signature_emp = models.CharField(max_length=200, blank=True, null=True)
    signature_direction = models.CharField(max_length=200, blank=True, null=True)
    signature_cell = models.CharField(max_length=200, blank=True, null=True)
    # For de-duping forms that have been edited.
    last_saved = models.DateTimeField(default=datetime.datetime.utcnow)

    # Meta class defines database table and labels, and clears any 
    # default permissions.
    class Meta:
        app_label = 'tracker'
        db_table = 'tracker_psychologicalexam'
        default_permissions = ()


"""Form for the PsychologicalExam model."""
class PsychologicalExamForm(ModelForm):
    # Meta class defines the fields and Spanish labels for the form.
    class Meta:
        model = PsychologicalExam
        
        fields = (
            'date',
            'family_notes',
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
            'family_notes': 'Antecedents Patológicos Personales y Familiares Importantes',
            'physical_description': 'Descripción Fisica y Comportamiento',
            'intellectual_notes': 'Área Intelectual',
            'organicity_notes': 'Área Organicidad',
            'psychomotor_notes': 'Área Psciomotor',
            'emotional_notes': 'Área Afectiva Emocional',
            ''
            'diagnosis': 'Diagnóstico',
            'recommendation': 'Recomendaciones',
            'priority': 'Prioridad',
        }
        widgets = {
            'date': DateInput(format='%d/%m/%Y'),
        }

    # Override __init__ so 'request' can be accessed in the clean() 
    # function.
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(PsychologicalExamForm, self).__init__(*args, **kwargs)

    # Override clean so forms can be saved without validating (so data 
    # isn't lost if the form can't be completed), but still raises 
    # exceptions when form is done incorrectly.
    def clean(self):
        msg = "Este campo es obligatorio."
        cleaned_data = super(PsychologicalExamForm, self).clean()
        
        # On validation ('submit' in request), checks if signature 
        # forms fields are filled out and raises exceptions on any 
        # fields left blank.
        if (self.request.POST):
            if ('submit' in self.request.POST):
                family_notes = cleaned_data.get('family_notes')
                if (family_notes == ''):
                    self.add_error('family_notes', msg)
                
                physical_description = cleaned_data.get('physical_description')
                if (physical_description == ''):
                    self.add_error('physical_description', msg)
                
                intellectual_notes = cleaned_data.get('intellectual_notes')
                if (intellectual_notes == ''):
                    self.add_error('intellectual_notes', msg)
                
                organicity_notes = cleaned_data.get('organicity_notes')
                if (organicity_notes == ''):
                    self.add_error('organicity_notes', msg)
                
                psychomotor_notes = cleaned_data.get('psychomotor_notes')
                if (psychomotor_notes == ''):
                    self.add_error('psychomotor_notes', msg)
                
                emotional_notes = cleaned_data.get('emotional_notes')
                if (emotional_notes == ''):
                    self.add_error('emotional_notes', msg)
                
                diagnosis = cleaned_data.get('diagnosis')
                if (diagnosis == ''):
                    self.add_error('diagnosis', msg)
                
                recommendation = cleaned_data.get('recommendation')
                if (recommendation == ''):
                    self.add_error('recommendation', msg)

