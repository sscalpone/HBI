# coding=utf-8

import datetime
import uuid

from django.contrib.auth.models import User
from django.db import models
from django.forms import ModelForm

from Child import Child
from Signature import Signature


"""The model to track the dental information of the children. Currently incomplete (still requiring visual representation of teeth). This model affects child priority.
"""
class DentalExam(models.Model):
    HIGH = 1
    MEDIUM = 2
    LOW = 3
    PRIORITY_CHOICES = (
        (HIGH, 'Alta Prioridad'),
        (MEDIUM, 'Prioridad Media'),
        (LOW, 'Prioridad Baja')
    )
    uuid = models.CharField(max_length=200, unique=True, default=uuid.uuid4)
    child = models.ForeignKey(Child)
    date = models.DateField()
    diagnosis = models.TextField(blank=True, null=True)
    recommendation = models.TextField(blank=True, null=True)
    priority = models.IntegerField(choices=PRIORITY_CHOICES, 
                                default=HIGH)
    signature = models.ForeignKey(Signature, blank=True, null=True)
    last_saved = models.DateTimeField() # for de-duping forms that have been edited.

    # Meta class defines database table and labels, and clears any default permissions.
    class Meta:
        app_label = 'tracker'
        db_table = 'tracker_dentalexam'
        default_permissions = ()


"""The form for the Dental model."""
class DentalExamForm(ModelForm):

    # Meta class defines the fields and Spanish labels for the form.
    class Meta:
        model = DentalExam
        fields = (
            'date',
            'diagnosis',
            'recommendation',
            'priority',
        )
        labels = {
            'date': 'Fecha',
            'diagnosis': 'Diagnóstico',
            'recommendation': 'Recomendaciones',
            'priority': 'Prioridad',
        }

    # Override __init__ so 'request' can be accessed in the clean() function.
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(DentalExamForm, self).__init__(*args, **kwargs)

    # Override clean so forms can be saved without validating (so data isn't lost if the form can't be completed), but still raises exceptions when form is done incorrectly.
    def clean(self):
        msg = "Este campo es obligatorio."
        cleaned_data = super(DentalExamForm, self).clean()

        # On validation ('submit' in request), checks if signature forms fields are filled out and raises exceptions on any fields left blank.
        if (self.request.method == 'POST'):
            if ('submit' in self.request.POST):
                diagnosis = cleaned_data.get('diagnosis')
                if (diagnosis == ''):
                    self.add_error('diagnosis', msg)
                recommendation = cleaned_data.get('recommendation')
                if (recommendation == ''):
                    self.add_error('recommendation', msg)



