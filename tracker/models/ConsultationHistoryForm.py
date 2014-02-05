import datetime

from ConsultationHistory import ConsultationHistory

from django.db import models

from django.contrib.auth.models import User

from django.forms import ModelForm


class ConsultationHistoryForm(ModelForm):
    class Meta:
        model = ConsultationHistory
        fields = '__all__'

