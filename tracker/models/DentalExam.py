# coding=utf-8

import datetime
import uuid

from django.db import models
from django.forms import ModelForm
from django.forms import DateInput

from Child import Child


"""The model to track the dental information of the children.
Currently incomplete (still requiring visual representation of teeth).
This model affects child priority. All fields are allowed to be saved
null so that forms can be saved before validation to prevent losing
information if the form can't be completed. This is overriden in the
clean() method.
"""


class DentalExam(models.Model):
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
    diagnosis = models.TextField(blank=True, null=True)
    completed_treatment = models.TextField(blank=True, null=True)
    recommendation = models.TextField(blank=True, null=True)
    priority = models.IntegerField(choices=PRIORITY_CHOICES,
                                   default=HIGH)
    signature_name = models.CharField(max_length=200, blank=True, null=True)
    signature_surname = models.CharField(max_length=200, blank=True,
                                         null=True)
    signature_emp = models.CharField(max_length=200, blank=True, null=True)
    signature_direction = models.CharField(max_length=200, blank=True,
                                           null=True)
    signature_cell = models.CharField(max_length=200, blank=True, null=True)
    # For de-duping forms that have been edited.
    last_saved = models.DateTimeField(default=datetime.datetime.utcnow)

    # Meta class defines database table and labels, and clears any
    # default permissions.
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
            'completed_treatment',
            'recommendation',
            'priority',
        )
        labels = {
            'date': 'Fecha',
            'diagnosis': 'Diagnóstico',
            'completed_treatment': 'Tratamiento Completada',
            'recommendation': 'Recomendaciones',
            'priority': 'Prioridad',
        }
        widgets = {
            'date': DateInput(attrs={
                'placeholder': 'DD/MM/AAAA',
                'format': 'DD/MM/AAAA'
            }),
        }

    # Override __init__ so 'request' can be accessed in the clean()
    # function.
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(DentalExamForm, self).__init__(*args, **kwargs)

    # Override clean so forms can be saved without validating (so data
    # isn't lost if the form can't be completed), but still raises
    # exceptions when form is done incorrectly.
    def clean(self):
        msg = "Este campo es obligatorio."
        cleaned_data = super(DentalExamForm, self).clean()

        # On validation ('submit' in request), checks if signature
        # forms fields are filled out and raises exceptions on any
        # fields left blank.
        if (self.request.POST):
            if ('submit' in self.request.POST):
                diagnosis = cleaned_data.get('diagnosis')
                if (diagnosis == ''):
                    self.add_error('diagnosis', msg)

                completed_treatment = cleaned_data.get('completed_treatment')
                if (completed_treatment == ''):
                    self.add_error('completed_treatment', msg)

                recommendation = cleaned_data.get('recommendation')
                if (recommendation == ''):
                    self.add_error('recommendation', msg)
