# coding=utf-8

import datetime
import uuid

from django.contrib.auth.models import User
from django.db import models
from django.forms import ModelForm
from django.forms import CheckboxInput
from django.forms import DateInput

from Child import Child


"""Model for the Social Exam, which keeps track of the children's 
social status, including family situations and legal status. This 
model affects child priority. This model references the Signature 
model and the Child model. All fields are allowed to be saved null so 
that forms can be saved before validation to prevent losing 
information if the form can't be completed. This is overriden in the 
clean() method.
"""
class SocialExam(models.Model):
    # The priority choices
    HIGH = 1
    MEDIUM = 2
    LOW = 3
    PRIORITY_CHOICES = (
        (HIGH, 'Alta Prioridad'),
        (MEDIUM, 'Prioridad Media'),
        (LOW, 'Prioridad Baja')
    )

    uuid = models.CharField(max_length=200, unique=True, default=uuid.uuid4)
    child = models.ForeignKey(Child, blank=True, null=True)
    date = models.DateField(default=datetime.date.today)
    has_birth_certificate = models.BooleanField(default=False)
    original_birth_certificate = models.BooleanField(default=False)
    dni = models.BooleanField(default=False)
    dni_in_process = models.BooleanField(default=False)
    sis = models.BooleanField(default=False)
    sis_in_process = models.BooleanField(default=False)
    dni_sis_no_comments = models.TextField(blank=True, null=True)
    antecedents = models.TextField(blank=True, null=True)
    family_situation = models.TextField(blank=True, null=True)
    general_comments = models.TextField(blank=True, null=True)
    visitors_allowed = models.BooleanField(default=True)
    visitors_allowed_no_comments = models.TextField(blank=True, null=True)
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
        db_table = 'tracker_socialexam'
        default_permissions = ()

"""The form for the Social Exam."""
class SocialExamForm(ModelForm):

    # Meta class defines the fields and Spanish labels for the form. 
    # Also defines any widgets being used.
    class Meta:
        model = SocialExam
        
        fields = (
            'date',
            'has_birth_certificate',
            'original_birth_certificate',
            'dni',
            'dni_in_process',
            'sis',
            'sis_in_process',
            'dni_sis_no_comments',
            'antecedents',
            'family_situation',
            'general_comments',
            'visitors_allowed',
            'visitors_allowed_no_comments',
            'diagnosis',
            'recommendation',
            'priority'
        )
        
        labels = {
            'date': "Fecha",
            'has_birth_certificate': "Partida de Nacimiento",
            'original_birth_certificate': "Original",
            'dni': "DNI",
            'dni_in_process': "En El Proceso",
            'sis': "SIS",
            'sis_in_process': "En El Proceso",
            'dni_sis_no_comments': "Comentarios",
            'antecedents': "Antecedentes",
            'family_situation': "Situación Familiar",
            'general_comments': "Apreciaciones Generales del Niño",
            'visitors_allowed': "Recibe Visitas",
            'visitors_allowed_no_comments': "Comentarios",
            'diagnosis': "Diagnostico Social",
            'recommendation': "Recomendaciones",
            'priority': 'Prioridad',
        }

        # Boolean fields represented with checkbox widgets in form.
        widgets = {
            'has_birth_certificate': CheckboxInput(),
            'original_birth_certificate': CheckboxInput(),
            'dni': CheckboxInput(),
            'dni_in_process': CheckboxInput(),
            'sis': CheckboxInput(),
            'sis_in_process': CheckboxInput(),
            'visitors_allowed': CheckboxInput(),
            'date': DateInput(format='%d/%m/%Y'),
        }

    # Override __init__ so 'request' can be accessed in the clean() 
    # function.
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(SocialExamForm, self).__init__(*args, **kwargs)

    # Override clean so forms can be saved without validating (so data 
    # isn't lost if the form can't be completed), but still raises 
    # exceptions when form is done incorrectly.
    def clean(self):
        msg = "Este campo es obligatorio."
        cleaned_data = super(SocialExamForm, self).clean()
        
        if (self.request.POST):
            
            # On validation ('submit' in request), checks if signature 
            # forms fields are filled out and raises exceptions on any 
            # fields left blank.
            if ('submit' in self.request.POST):
                
                antecedents = cleaned_data.get('antecedents')
                if (antecedents == ''):
                    self.add_error('antecedents', msg)
                
                family_situation = cleaned_data.get('family_situation')
                if (family_situation == ''):
                    self.add_error('family_situation', msg)
                
                general_comments = cleaned_data.get('general_comments')
                if (general_comments == ''):
                    self.add_error('general_comments', msg)
                
                diagnosis = cleaned_data.get('diagnosis')
                if (diagnosis == ''):
                    self.add_error('diagnosis', msg)
                
                recommendation = cleaned_data.get('recommendation')
                if (recommendation == ''):
                    self.add_error('recommendation', msg)

                # If the child does not have an Identity Card (DNI) or 
                # public health insurance (SIS), there must be an 
                # explanation, and child must be automatically high 
                # priority.
                dni = cleaned_data.get('dni')
                dni_in_process = cleaned_data.get('dni_in_process')
                sis = cleaned_data.get('sis')
                sis_in_process = cleaned_data.get('sis_in_process')
                dni_sis_no_comments = cleaned_data.get('dni_sis_no_comments')
                priority = cleaned_data.get('priority')
                if (not dni and not sis_in_process and 
                    dni_sis_no_comments == ''):
                    self.add_error('dni_sis_no_comments', msg)
                if (not dni and not sis and priority is not 1):
                    self.add_error('priority', 
                        'Sin un DNI o SIS , niño debe ser etiquetado de alta '
                        'prioridad.')   

                # If the child is not allowed visiters, there must be 
                # an explanation.
                visitors_allowed = cleaned_data.get('visitors_allowed')
                visitors_allowed_no_comments = cleaned_data.get(
                    'visitors_allowed_no_comments')
                if (not visitors_allowed and 
                    visitors_allowed_no_comments == ''):
                    self.add_error('visitors_allowed_no_comments', msg)


