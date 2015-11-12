# coding=utf-8

import datetime
import uuid

from django.contrib.auth.models import User
from django.db import models
from django.forms import ModelForm

from Child import Child
from Signature import Signature

class ConsultationHistory(models.Model):
	uuid = models.CharField(max_length=200, unique=True, default=uuid.uuid4)
	child = models.ForeignKey(Child)
	date = models.DateField()
	institution = models.CharField(max_length=200, blank=True, null=True)
	notes = models.TextField(blank=True, null=True)
	signature = models.ForeignKey(Signature, blank=True, null=True)
	last_saved = models.DateTimeField()

	class Meta:
		app_label='tracker'
		db_table='tracker_consultationhistory'
		default_permissions = ()


class ConsultationHistoryForm(ModelForm):
	class Meta:
		model = ConsultationHistory
		fields = (
			'date',
			'institution',
			'notes',
		)
		labels = {
			'date': 'Fecha',
			'institution': 'Institución',
			'notes': 'Comentarios'
		}

	def __init__(self, *args, **kwargs):
		self.request = kwargs.pop('request', None)
		super(ConsultationHistoryForm, self).__init__(*args, **kwargs)

	def clean(self):
		msg = "Este campo es obligatorio."
		cleaned_data = super(ConsultationHistoryForm, self).clean()

		if self.request.POST:
			if 'submit' in self.request.POST:
				institution = cleaned_data.get('institution')
				if institution=='':
					self.add_error('institution', msg)
				notes = cleaned_data.get('notes')
				if notes=='':
					self.add_error('notes', msg)






