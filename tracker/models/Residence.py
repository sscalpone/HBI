# coding=utf-8

import datetime
import uuid

from django.contrib.auth.models import User
from django.db import models
from django.forms import ModelForm

class Residence(models.Model):
	uuid = models.CharField(max_length=200, unique=True, default=uuid.uuid4)
	residence_name = models.CharField(max_length=200, blank=True, null=True)
	administrator = models.CharField(max_length=200, blank=True, null=True)
	location = models.CharField(max_length=200, blank=True, null=True)
	last_saved = models.DateTimeField()

	def __unicode__(self):
		return self.residence_name

	class Meta:
		app_label = 'tracker'
		db_table = 'tracker_residence'
		default_permissions = ()


class ResidenceForm(ModelForm):
	class Meta:
		model = Residence
		fields = (
			'residence_name',
			'administrator',
			'location',
			)
		labels = {
			'residence_name': 'Casa Girasoles',
			'administrator': 'Administrador',
			'location': 'Localización',
			}

	def __init__(self, *args, **kwargs):
		self.request = kwargs.pop('request', None)
		super(ResidenceForm, self).__init__(*args, **kwargs)

	def clean(self):
		msg = "Este campo es obligatorio."
		cleaned_data = super(ResidenceForm, self).clean()

		if self.request.method=='POST':
			if 'submit' in self.request.POST:
				residence_name = cleaned_data.get('residence_name')
				if residence_name=='':
					self.add_error('residence_name', msg)
				location = cleaned_data.get('location')
				if location=='':
					self.add_error('location', msg)
				administrator = cleaned_data.get('administrator')
				if administrator=='':
					self.add_error('administrator', msg)




