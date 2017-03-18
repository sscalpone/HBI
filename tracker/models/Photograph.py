# coding=utf-8

import datetime
import uuid

from django.db import models
from django.forms import ModelForm
from django.forms import DateInput

from Child import Child


"""The Photograph models stores any extra photos of the children the
users want to upload (profile photo is stored in the Child model). It
references the Child model. All fields are allowed to be saved null so
that forms can be saved before validation to prevent losing
information if the form can't be completed. This is overriden in the
clean() method.
"""

class Photograph(models.Model):
    uuid = models.CharField(max_length=200, unique=True, default=uuid.uuid4)
    child = models.ForeignKey(Child, blank=True, null=True)
    date = models.DateField(default=datetime.date.today)
    photo = models.ImageField(upload_to='photos', blank=True, null=True)

    # For de-duping forms that have been edited.
    last_saved = models.DateTimeField(default=datetime.datetime.utcnow)

    # Meta class defines database table and labels, and clears any
    # default permissions.
    class Meta:
        app_label = 'tracker'
        db_table = 'tracker_photograph'
        default_permissions = ()


"""Form for the Photograph model."""

class PhotographForm(ModelForm):
    # Meta class defines the fields and Spanish labels for the form.
    class Meta:
        model = Photograph

        fields = (
            'date',
            'photo',
        )

        labels = {
            'date': 'Fecha',
            'photo': 'Fotografía',
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
        super(PhotographForm, self).__init__(*args, **kwargs)

    # Override clean so forms can be saved without validating (so data
    # isn't lost if the form can't be completed), but still raises
    # exceptions when form is done incorrectly.
    def clean(self):
        msg = "Este campo es obligatorio."
        cleaned_data = super(PhotographForm, self).clean()

        # On validation ('submit' in request), checks if signature
        # forms fields are filled out and raises exceptions on any
        # fields left blank.
        if (self.request.POST):
            if ('submit' in self.request.POST):
                photo = cleaned_data.get('photo')
                if (photo is None):
                    self.add_error('photo', msg)
