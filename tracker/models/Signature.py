# coding=utf-8

import datetime
import uuid

from django.db import models
from django.forms import ModelForm


"""Model for the record of who is filling out each form. Each form has 
a signature_id to reference the signature of that form. All fields are 
allowed to be saved null so that forms can be saved before validation 
to prevent losing information if the form can't be completed. This is 
overriden in the clean() method.
"""
class Signature(models.Model):
    uuid = models.CharField(max_length=200, unique=True, default=uuid.uuid4)
    name = models.CharField(max_length=200, blank=True, null=True)
    surname = models.CharField(max_length=200, blank=True, null=True)
    emp = models.CharField(max_length=200, blank=True, null=True)
    direction = models.CharField(max_length=200, blank=True, null=True)
    cell = models.CharField(max_length=200, blank=True, null=True)
    # For de-duping forms that have been edited.
    last_saved = models.DateTimeField(blank=True, null=True)

    # Meta class defines database table and labels, and clears any 
    # default permissions.
    class Meta:
        app_label = 'tracker'
        db_table = 'tracker_signature'
        default_permissions = ()

    # The human-readable version of the signature - the name of the 
    # person filling out the form.
    def __unicode__(self):
        return self.name


"""The form for the signature. Attached at the end of every exam form.
"""
class SignatureForm(ModelForm):
    # Meta class defines the fields and Spanish labels for the form.
    class Meta:
        model = Signature
        
        fields = (
            'name',
            'surname',
            'emp',
            'direction',
            'cell',
        )

        labels = {
            'name': 'Nombres',
            'surname': 'Apellidos',
            'emp': 'EMP',
            'direction': 'Direccion',
            'cell': 'Celular',
        }

    # Override __init__ so 'request' can be accessed in the clean() 
    # function.
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(SignatureForm, self).__init__(*args, **kwargs)

    # Override clean so forms can be saved without validating (so data 
    # isn't lost if the form can't be completed), but still raises 
    # exceptions when form is done incorrectly.
    def clean(self):
        msg = "Este campo es obligatorio." # Validation exception message
        cleaned_data = super(SignatureForm, self).clean()
        
        # On validation ('submit' in request), checks if signature 
        # forms fields are filled out and raises exceptions on any 
        # fields left blank.
        if (self.request.POST):
            if ('submit' in self.request.POST):
                
                name = cleaned_data.get('name')
                if (name == ''):
                    self.add_error('name', msg)
                
                surname = cleaned_data.get('surname')
                if (surname == ''):
                    self.add_error('surname', msg)
                
                emp = cleaned_data.get('emp')
                if (emp == ''):
                    self.add_error('emp', msg)
                
                direction = cleaned_data.get('direction')
                if (direction == ''):
                    self.add_error('direction', msg)

                cell = cleaned_data.get('cell')
                if (cell == ''):
                    self.add_error('cell', msg)


