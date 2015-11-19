# coding=utf-8

import datetime
import uuid

from django.contrib.auth.models import User
from django.db import models
from django.forms import ModelForm
from django.forms import CheckboxInput

from Residence import Residence


"""The Child model stores the basic information of each child saved in the database. It includes a function to calculate age. Child priority is saved in this model but cannot be set programmatically (set in exam_views.py). The residence ForeignKey references the Residence model: it saves the information about the house they live in.
"""
class Child(models.Model):
    # The gender choices for the children
    MALE = 'm'
    FEMALE = 'f'
    GENDER_CHOICES = (
        (MALE, 'Hombre'),
        (FEMALE, 'Mujer')
    )
    
    # The priority choices
    HIGH = 1
    MEDIUM = 2
    LOW = 3
    PRIORITY_CHOICES = (
        (HIGH, 'Alta Prioridad'),
        (MEDIUM, 'Prioridad Media'),
        (LOW, 'Prioridad Baja')
    )
    
    # The fields
    uuid = models.CharField(max_length=200, unique=True, default=uuid.uuid4)
    residence = models.ForeignKey(Residence, default=1, blank=True, null=True)
    first_name = models.CharField(max_length=200, blank=True, null=True)
    last_name = models.CharField(max_length=200, blank=True, null=True)
    nickname = models.CharField(max_length=200, blank=True, null=True)
    birthdate = models.DateField(blank=True, null=True)
    gender = models.CharField(max_length=6, 
                              choices=GENDER_CHOICES, 
                              default=MALE)
    birthplace = models.CharField(max_length=200, blank=True, null=True)
    intake_date = models.DateField(blank=True, null=True)
    discharge_date = models.DateField(blank=True, null=True)
    photo = models.ImageField(upload_to='photos', blank=True, null=True)
    priority = models.IntegerField(choices=PRIORITY_CHOICES, 
                                default=LOW)
    active = models.BooleanField(default=True)
    last_saved = models.DateTimeField()

    # Meta class defines database table and labels, and clears any default permissions.
    class Meta:
        app_label = 'tracker'
        db_table = 'tracker_child'
        verbose_name_plural = "Children"
        default_permissions = ()

    # Human-readable version of the model - Child's first name.
    def __unicode__(self):
        return self.first_name

    # Calculates age of child in years based on age_in_years() function.
    def age(self):
        return self.age_in_years(self.birthdate, datetime.datetime.utcnow())

    # Calculates age in years of child based on birthday and whether the birthday is on a leap day or not.
    def age_in_years(self, from_date, to_date, leap_day_anniversary_Feb28=True):
        computed_age = to_date.year - from_date.year
        try:
            anniversary = from_date.replace(year=to_date.year)
        except ValueError:
            assert from_date.day == 29 and from_date.month == 2
            if (leap_day_anniversary_Feb28):
                anniversary = datetime.date(to_date.year, 2, 28)
            else:
                anniversary = datetime.date(to_date.year, 3, 1)
            if (to_date < anniversary):
                computed_age -= 1
        return computed_age


"""Form for the Child model."""
class ChildForm(ModelForm):

    # Meta class defines the fields and Spanish labels for the form. Also defines any weidgets being used.
    class Meta:
        model = Child
        
        fields = (
            'residence',
            'first_name',
            'last_name',
            'nickname',
            'birthdate',
            'gender',
            'birthplace',
            'intake_date',
            'discharge_date',
            'photo',
            'active',
        )
        
        labels = {
            'residence': 'Casa Girasoles',
            'first_name': 'Nombres',
            'last_name': 'Apellidos',
            'nickname': 'Apodo',
            'birthdate': 'Fecha de Naciemiento',
            'gender': 'Género',
            'birthplace': 'Lugar de Naciemiento',
            'intake_date': 'Fecha de Ingreso',
            'discharge_date': 'Fecha de Salida',
            'photo': 'Fotografía',
            'active': 'Activo',
        }

        widgets = {
            'active': CheckboxInput(),
        }

    # Override __init__ so 'request' can be accessed in the clean() function.
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(ChildForm, self).__init__(*args, **kwargs)

    # Override clean so forms can be saved without validating (so data isn't lost if the form can't be completed), but still raises exceptions when form is done incorrectly.
    def clean(self):
        msg = "Este campo es obligatorio."
        cleaned_data = super(ChildForm, self).clean()

        # On validation ('submit' in request), checks if signature forms fields are filled out and raises exceptions on any fields left blank.
        if (self.request.method == 'POST'):
            if ('submit' in self.request.POST):
                
                residence = cleaned_data.get('residence')
                if (residence is None):
                    self.add_error('residence', msg)
                
                first_name = cleaned_data.get('first_name')
                if (first_name == ''):
                    self.add_error('first_name', msg)
                
                last_name = cleaned_data.get('last_name')
                if (last_name == ''):
                    self.add_error('last_name', msg)
                
                birthdate = cleaned_data.get('birthdate')
                if (birthdate is None):
                    self.add_error('birthdate', msg)
                
                birthplace = cleaned_data.get('birthplace')
                if (birthplace == ''):
                    self.add_error('birthplace', msg)
                
                intake_date = cleaned_data.get('intake_date')
                if (intake_date is None):
                    self.add_error('intake_date', msg)

                photo = cleaned_data.get('photo')
                if (photo is None):
                    self.add_error('photo', msg)
                
                # Checks that inactive children have discharge date
                discharge_date = cleaned_data.get('discharge_date')
                active = cleaned_data('active')
                if (not active and discharge_date is None):
                    self.add_error('discharge_date', msg)

                # Checks that active children do not have discharge date
                if (active and discharge_date is not None):
                    self.add_error('discharge_date', 'Sin fecha de alta se puede especificar para niños activos.')

