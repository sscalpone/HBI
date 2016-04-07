# coding=utf-8

import datetime
import uuid

from django.contrib.auth.models import User
from django import forms

class ImportDBForm(forms.Form):
    upload = forms.FileField()