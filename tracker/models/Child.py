# coding=utf-8

import datetime

from django.contrib.auth.models import User
from django.db import models
from django.forms import ModelForm

from Residence import Residence

class Child(models.Model):
    residence = models.ForeignKey(Residence)
    first_name = models.CharField(max_length=200, null=True)
    last_name = models.CharField(max_length=200, null=True)
    birthdate = models.DateField(null=True)
    birthplace = models.CharField(max_length=200, null=True)
    intake_date = models.DateField(null=True)
    photo = models.ImageField(upload_to='photos', null=True)

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
            'birthplace',
            'intake_date',
            'photo',
        )
        labels = {
            'residence': 'Casa Girasoles',
            'first_name': 'Nombres',
            'last_name': 'Apellidos',
            'birthdate': 'Fecha de Naciemiento',
            'birthplace': 'Lugar de Naciemiento',
            'intake_date': 'Fecha de Ingreso',
            'photo': 'Fotografía',
        }

