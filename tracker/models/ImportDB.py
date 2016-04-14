# coding=utf-8

import datetime
import uuid

from CustomUser import CustomUser as User
from django import forms
from django.forms import CheckboxInput
from django.forms import DateInput

class ImportDBForm(forms.Form):
	upload = forms.FileField(label='Subir')
	fix =  forms.BooleanField(initial=False, required=False, label='Correcta importación anterior (no se recomienda):', widget=forms.CheckboxInput)