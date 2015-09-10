# coding=utf-8

import datetime

from django.contrib.auth.models import User
from django.db import models
from django.forms import ModelForm

class Residence(models.Model):
    residence_name = models.CharField(max_length=200)

    def __unicode__(self):
        return self.residence_name

    class Meta:
        app_label = 'tracker'
        db_table = 'tracker_residence'

class ResidenceForm(ModelForm):
	class Meta:
		model = Residence
		fields = (
			'residence_name',
			)
		labels = {
			'residence_name': 'Casa Girasoles',
			}