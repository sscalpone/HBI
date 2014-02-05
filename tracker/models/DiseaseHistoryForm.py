import datetime

from DiseaseHistory import DiseaseHistory

from django.db import models

from django.contrib.auth.models import User

from django.forms import ModelForm


class DiseaseHistoryForm(ModelForm):
    class Meta:
        model = DiseaseHistory
        fields = '__all__'

