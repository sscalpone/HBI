# coding=utf-8

import datetime
from Child import Child
from django.db import models
from django.forms import ModelForm


class ChildForm(ModelForm):
    class Meta:
        model = Child
        fields = '__all__'
        labels = {
            'residence': 'Casa Girasoles',
            'first_name': 'Nombres',
            'last_name': 'Apellidos',
            'birthdate': 'Fecha de Naciemiento',
            'birthplace': 'Lugar de Naciemiento',
            'intake_date': 'Fecha de Ingreso',
            'photo': 'Fotografía',
        }

