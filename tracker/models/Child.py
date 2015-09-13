# coding=utf-8

import datetime

from django.contrib.auth.models import User
from django.db import models
from django.forms import ModelForm
from django.forms import CheckboxInput

from Residence import Residence

class Child(models.Model):
    MALE = 'm'
    FEMALE = 'f'
    GENDER_CHOICES = (
        (MALE, 'Hombre'),
        (FEMALE, 'Mujer')
    )
    HIGH = 1
    MEDIUM = 2
    LOW = 3
    PRIORITY_CHOICES = (
        (HIGH, 'Alta Prioridad'),
        (MEDIUM, 'Prioridad Media'),
        (LOW, 'Prioridad Baja')
    )
    residence = models.ForeignKey(Residence, default=1, blank=True, null=True)
    first_name = models.CharField(max_length=200, blank=True, null=True)
    last_name = models.CharField(max_length=200, blank=True, null=True)
    birthdate = models.DateField(blank=True, null=True)
    gender = models.CharField(max_length=6, 
                              choices=GENDER_CHOICES, 
                              default=MALE)
    birthplace = models.CharField(max_length=200, blank=True, null=True)
    intake_date = models.DateField(blank=True, null=True)
    photo = models.ImageField(upload_to='photos', default='/media/photos/person-icon.svg', blank=True, null=True)
    priority = models.IntegerField(choices=PRIORITY_CHOICES, 
                                default=LOW)
    active = models.BooleanField(default=True)

    class Meta:
        app_label = 'tracker'
        db_table = 'tracker_child'
        verbose_name_plural = "Children"

    def __unicode__(self):
        return self.first_name

    def age(self):
        return self.age_in_years(self.birthdate, datetime.datetime.utcnow())

    def age_in_years(self, from_date, to_date, leap_day_anniversary_Feb28=True):
        computed_age = to_date.year - from_date.year
        try:
            anniversary = from_date.replace(year=to_date.year)
        except ValueError:
            assert from_date.day == 29 and from_date.month == 2
            if leap_day_anniversary_Feb28:
                anniversary = datetime.date(to_date.year, 2, 28)
            else:
                anniversary = datetime.date(to_date.year, 3, 1)
            if to_date < anniversary:
                computed_age -= 1
        return computed_age


class ChildForm(ModelForm):
    class Meta:
        model = Child
        fields = (
            'residence',
            'first_name',
            'last_name',
            'birthdate',
            'gender',
            'birthplace',
            'intake_date',
            'photo',
            'active',
        )
        labels = {
            'residence': 'Casa Girasoles',
            'first_name': 'Nombres',
            'last_name': 'Apellidos',
            'birthdate': 'Fecha de Naciemiento',
            'gender': 'Género',
            'birthplace': 'Lugar de Naciemiento',
            'intake_date': 'Fecha de Ingreso',
            'photo': 'Fotografía',
            'active': 'Activo',
        }
        widgets = {
            'active': CheckboxInput(),
        }

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(ChildForm, self).__init__(*args, **kwargs)


    def clean(self):
        msg = "Este campo es obligatorio."
        cleaned_data = super(ChildForm, self).clean()

        if self.request.method=='POST':
            if 'submit' in self.request.POST:
                residence = cleaned_data.get('residence')
                if residence is None:
                    self.add_error('residence', msg)
                first_name = cleaned_data.get('first_name')
                if first_name=='':
                    self.add_error('first_name', msg)
                last_name = cleaned_data.get('last_name')
                if last_name=='':
                    self.add_error('last_name', msg)
                birthdate = cleaned_data.get('birthdate')
                if birthdate=='':
                    self.add_error('birthdate', msg)
                birthplace = cleaned_data.get('birthplace')
                if birthplace=='':
                    self.add_error('birthplace', msg)
                intake_date = cleaned_data.get('intake_date')
                if intake_date=='':
                    self.add_error('intake_date', msg)
                photo = cleaned_data.get('photo')
                if photo is None:
                    self.add_error('photo', msg)

