import datetime

from Child import Child

from django.db import models

from django.contrib.auth.models import User

from django.forms import ModelForm


class ChildForm(ModelForm):
    class Meta:
        model = Child
        fields = '__all__'

