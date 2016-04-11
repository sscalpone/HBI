# coding=utf-8

import datetime
import uuid

from django.contrib.auth.models import User
from django.db import models
from django.forms import ModelForm

from Child import Child
from Signature import Signature


"""Model for the Dicharge Plan, which evaluates the child's plans after
they have been dicharged. This model references the Signature model and
the Child model. All fields are allowed to be saved null so that forms 
can be saved before validation to prevent losing information if the 
form can't be completed. This is overriden in the clean() method.
"""
class DischargePlan(models.Model):

    uuid = models.CharField(max_length=200, unique=True, default=uuid.uuid4)
    child = models.ForeignKey(Child)
    date = models.DateField()
    summary = models.TextField(blank=True, null=True)
    strengths_challenges = models.TextField(blank=True, null=True)
    family = models.TextField(blank=True, null=True)
    training = models.TextField(blank=True, null=True)
    future_housing = models.TextField(blank=True, null=True)
    signature = models.ForeignKey(Signature, blank=True, null=True)
    # For de-duping forms that have been edited.
    last_saved = models.DateTimeField(blank=True, null=True)

    # Meta class defines database table and labels, and clears any 
    # default permissions.
    class Meta:
        app_label = 'tracker'
        db_table = 'tracker_dischargeplan'
        default_permissions = ()

"""The form for the Discharge Plan."""
class DischargePlanForm(ModelForm):

    # Meta class defines the fields and Spanish labels for the form. 
    # Also defines any widgets being used.
    class Meta:
        model = DischargePlan
        
        fields = (
            'date',
            'summary',
            'strengths_challenges',
            'family',
            'training',
            'future_housing',
        )
        
        labels = {
            'date': "Fecha",
            'summary': 'Resumen del Niño(a) - Salud mental, físico, y emocional.',
            'strengths_challenges': 'Fuerzas, Desafios, Consideraciones Especiales, etc.',
            'family': 'Relaciones Familiares o Comunitarias',
            'training': 'Enfoque de formación profesional (es decir, educación superior, militar, manual laboral, gastronomía, etc.)',
            'future_housing': 'Futuras posibilidades de alojamiento', 
        }


    # Override __init__ so 'request' can be accessed in the clean() 
    # function.
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(DischargePlanForm, self).__init__(*args, **kwargs)

    # Override clean so forms can be saved without validating (so data 
    # isn't lost if the form can't be completed), but still raises 
    # exceptions when form is done incorrectly.
    def clean(self):
        msg = "Este campo es obligatorio."
        cleaned_data = super(DischargePlanForm, self).clean()
        
        if (self.request.POST):
            
            # On validation ('submit' in request), checks if signature 
            # forms fields are filled out and raises exceptions on any 
            # fields left blank.
            if ('submit' in self.request.POST):
                
                summary = cleaned_data.get('summary')
                if (summary == ''):
                    self.add_error('summary', msg)

                strengths_challenges = cleaned_data.get('strengths_challenges')
                if (strengths_challenges == ''):
                    self.add_error('strengths_challenges', msg)

                family = cleaned_data.get('family')
                if (family == ''):
                    self.add_error('family', msg)

                training = cleaned_data.get('training')
                if (training == ''):
                    self.add_error('training', msg)

                future_housing = cleaned_data.get('future_housing')
                if (future_housing == ''):
                    self.add_error('future_housing', msg)



