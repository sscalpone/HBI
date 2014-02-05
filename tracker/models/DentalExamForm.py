import datetime

from DentalExam import DentalExam

from django.db import models

from django.forms import ModelForm

class DentalExamForm(ModelForm):
    class Meta:
        model = DentalExam
        fields = '__all__'

