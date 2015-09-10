# coding=utf-8

import datetime

from django.contrib.auth.models import User
from django.db import models
from django.forms import ModelForm

from Child import Child
from Signature import Signature


class DentalExam(models.Model):
    child = models.ForeignKey(Child)
    date = models.DateField()
    recommendation = models.TextField(blank=True, null=True)

    class Meta:
        app_label = 'tracker'
        db_table = 'tracker_dentalexam'


class DentalExamDiagnosis(models.Model):
    exam = models.ForeignKey(DentalExam)
    diagnosis_notes = models.TextField()

    class Meta:
        app_label = 'tracker'
        db_table = 'tracker_dentalexamdiagnosis'


class DentalExamForm(ModelForm):
    class Meta:
        model = DentalExam
        fields = (
            'date',
            'recommendation',
        )
        labels = {
            'date': 'Fecha',
            'recommendation': 'Recomendaciones',
        }

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(DentalExamForm, self).__init__(*args, **kwargs)

    def clean(self):
        msg = "This field is required."
        cleaned_data = super(DentalExamForm, self).clean()

        if self.request.method == 'POST':
            recommendation = cleaned_data.get('recommendation')
            if 'submit' in self.request.POST:
                if recommendation=='':
                    self.add_error('recommendation', msg)



