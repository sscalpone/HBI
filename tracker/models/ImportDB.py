# coding=utf-8

import datetime
import uuid

from CustomUser import CustomUser as User
from django import forms
from django.forms import CheckboxInput

class ImportDBForm(forms.Form):
	upload = forms.FileField()