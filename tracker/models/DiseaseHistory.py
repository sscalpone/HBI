# coding=utf-8

import datetime
import uuid

from django.contrib.auth.models import User
from django.db import models
from django.forms import ModelForm

from Child import Child
from Signature import Signature

class DiseaseHistory(models.Model):
	uuid = models.CharField(max_length=200, unique=True, default=uuid.uuid4)
	child = models.ForeignKey(Child)
	date = models.DateField()
	institution = models.CharField(max_length=200, null=True, blank=True)
	diagnosis = models.TextField(null=True, blank=True)
	studies = models.TextField(null=True, blank=True)
	treatment = models.TextField(null=True, blank=True)
	signature = models.ForeignKey(Signature, blank=True, null=True)
	last_saved = models.DateTimeField()

	class Meta:
		app_label='tracker'
		db_table='tracker_diseasehistory'
		default_permissions = ()


class DiseaseHistoryForm(ModelForm):
	class Meta:
		model = DiseaseHistory
		fields = (
			'date',
			'institution',
			'diagnosis',
			'studies',
			'treatment',
		)
		labels = {
			'date': 'Fecha',
			'institution': 'Institución',
			'diagnosis': 'Diagnóstico',
			'studies': 'Estudios',
			'treatment': 'Tratamiento',
		}

	def __init__(self, *args, **kwargs):
		self.request = kwargs.pop('request', None)
		super(DiseaseHistoryForm, self).__init__(*args, **kwargs)

	def clean(self):
		msg = "Este campo es obligatorio."
		cleaned_data = super(DiseaseHistoryForm, self).clean()
		if self.request.POST:
			if 'submit' in self.request.POST:
				institution = cleaned_data.get('institution')
				if institution=='':
					self.add_error('institution', msg)
				diagnosis = cleaned_data.get('diagnosis')
				if diagnosis=='':
					self.add_error('diagnosis', msg)
				studies = cleaned_data.get('studies')
				if studies=='':
					self.add_error('studies', msg)
				treatment = cleaned_data.get('treatment')
				if treatment=='':
					self.add_error('treatment', msg)







