# coding=utf-8

from tracker.models import OperationHistory
from django.forms import ModelForm


class OperationHistoryForm(ModelForm):
    class Meta:
        model = OperationHistory
        fields = '__all__'

