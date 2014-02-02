import datetime

from OperationHistory import OperationHistory

from django.db import models

from django.contrib.auth.models import User

from django.forms import ModelForm


class OperationHistoryForm(ModelForm):
    class Meta:
        model = OperationHistory
        fields = '__all__'

