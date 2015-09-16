# coding=utf-8

import datetime

from django.contrib.auth.models import User
from django.db import models
from django.forms import ModelForm

from Child import Child
from Signature import Signature

class OperationHistory(models.Model):
	child = models.ForeignKey(Child)
	date = models.DateField()
	institution = models.CharField(max_length=200, blank=True, null=True)
	preop_diagnosis = models.TextField(blank=True, null=True)
	intervention = models.TextField(blank=True, null=True)
	postop_diagnosis = models.TextField(blank=True, null=True)
	signature = models.ForeignKey(Signature, blank=True, null=True)

	class Meta:
		app_label='tracker'
		db_table='tracker_operationhistory'

class OperationHistoryForm(ModelForm):
	class Meta:
		model = OperationHistory
		fields = (
			'date',
			'institution',
			'preop_diagnosis',
			'intervention',
			'postop_diagnosis',
		)
		labels = {
			'date': 'Fecha',
			'institution': 'Institución',
			'preop_diagnosis':'Diagnóstico Preoperatorio',
			'intervention': 'Intervención',
			'postop_diagnosis': 'Diagnóstico Postoperatorio',
		}

	def __init__(self, *args, **kwargs):
		self.request = kwargs.pop('request', None)
        super(OperationHistoryForm, self).__init__(*args, **kwargs)

	def clean(self):
		msg = "Este campo es obligatorio."
    	cleaned_data = super(OperationHistoryForm, self).clean()
        if self.request.POST:
        	if 'submit' in self.request.POST:
        		institution = cleaned_data.get('institution')
        		if institution == '':
        			self.add_error('institution', msg)
        		preop_diagnosis = cleaned_data.get('preop_diagnosis')
        		if preop_diagnosis == '':
        			self.add_error('preop_diagnosis', msg)
        		intervention = cleaned_data.get('intervention')
        		if intervention == '':
        			self.add_error('intervention', msg)
        		postop_diagnosis = cleaned_data.get('postop_diagnosis')
        		if postop_diagnosis == '':
        			self.add_error('postop_diagnosis', msg)




