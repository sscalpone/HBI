# coding=utf-8

import datetime
import uuid

from django.db import models
from django.forms import ModelForm
from django.forms import DateInput

from Child import Child


"""Model for the Education Plan, which evaluates the child's plans for
education. This model references the Signature model and
the Child model. All fields are allowed to be saved null so that forms
can be saved before validation to prevent losing information if the
form can't be completed. This is overriden in the clean() method.
"""

class EducationPlan(models.Model):

    uuid = models.CharField(max_length=200, unique=True, default=uuid.uuid4)
    child = models.ForeignKey(Child, blank=True, null=True)
    date = models.DateField(default=datetime.date.today)
    diagnosis = models.TextField(blank=True, null=True)
    standards = models.TextField(blank=True, null=True)
    instruction = models.TextField(blank=True, null=True)
    growth = models.TextField(blank=True, null=True)
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
        db_table = 'tracker_educationplan'
        default_permissions = ()


"""The form for the Education Plan."""

class EducationPlanForm(ModelForm):

    # Meta class defines the fields and Spanish labels for the form.
    # Also defines any widgets being used.
    class Meta:
        model = EducationPlan

        fields = (
            'date',
            'diagnosis',
            'standards',
            'instruction',
            'growth',
        )

        labels = {
            'date': "Fecha",
            'diagnosis':  ('Diagnóstico: Evaluar las fortalezas, '
                           'debilidades, conocimientos, habilidades del'
                           ' estudiante antes de la instrucción'),
            'standards': ('Referencia a Normas: Compara el rendimiento de un'
                          ' estudiante contra otros alumnos (un grupo '
                          'nacional u otra "norma")'),
            'instruction': ('Formativa: Evalúa el rendimiento de un '
                            'estudiante durante la instrucción'),
            'growth': ('Crecimiento: Mide el logro de un estudiante'
                       ' al final de la instrucción.'),
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
        super(EducationPlanForm, self).__init__(*args, **kwargs)

    # Override clean so forms can be saved without validating (so data
    # isn't lost if the form can't be completed), but still raises
    # exceptions when form is done incorrectly.
    def clean(self):
        msg = "Este campo es obligatorio."
        cleaned_data = super(EducationPlanForm, self).clean()

        if (self.request.POST):

            # On validation ('submit' in request), checks if signature
            # forms fields are filled out and raises exceptions on any
            # fields left blank.
            if ('submit' in self.request.POST):

                diagnosis = cleaned_data.get('diagnosis')
                if (diagnosis == ''):
                    self.add_error('diagnosis', msg)

                standards = cleaned_data.get('standards')
                if (standards == ''):
                    self.add_error('standards', msg)

                instruction = cleaned_data.get('instruction')
                if (instruction == ''):
                    self.add_error('instruction', msg)

                growth = cleaned_data.get('growth')
                if (growth == ''):
                    self.add_error('growth', msg)
