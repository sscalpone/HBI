# coding=utf-8

import datetime
import uuid

from django.contrib.auth.models import User
from django.db import models
from django.forms import ModelForm

from Child import Child
from Signature import Signature


"""The OperationHistory model holds information about each child's 
past operations, if any. It details the pre- and post-op diagnoses and 
type of operation. It references the Child model and the Signature 
model. All fields are allowed to be saved null so that forms can be 
saved before validation to prevent losing information if the form 
can't be completed. This is overriden in the clean() method.
"""
class OperationHistory(models.Model):
	uuid = models.CharField(max_length=200, unique=True, default=uuid.uuid4)
	child = models.ForeignKey(Child)
	date = models.DateField()
	institution = models.CharField(max_length=200, blank=True, null=True)
	preop_diagnosis = models.TextField(blank=True, null=True)
	intervention = models.TextField(blank=True, null=True)
	postop_diagnosis = models.TextField(blank=True, null=True)
	follow_up = models.TextField(blank=True, null=True)
	signature = models.ForeignKey(Signature, blank=True, null=True)
	# For de-duping forms that have been edited.
	last_saved = models.DateTimeField(blank=True, null=True)

    # Meta class defines database table and labels, and clears any 
    # default permissions.
	class Meta:
		app_label='tracker'
		db_table='tracker_operationhistory'
		default_permissions = ()


"""Form for the OperationHistory model."""
class OperationHistoryForm(ModelForm):
	# Meta class defines the fields and Spanish labels for the form.
	class Meta:
		model = OperationHistory
		
		fields = (
			'date',
			'institution',
			'preop_diagnosis',
			'intervention',
			'postop_diagnosis',
			'follow_up',
		)
		
		labels = {
			'date': 'Fecha',
			'institution': 'Institución',
			'preop_diagnosis': 'Diagnóstico Preoperatorio',
			'intervention': 'Intervención',
			'postop_diagnosis': 'Diagnóstico Postoperatorio',
			'follow_up': 'Seguimiento',
		}

	# Override __init__ so 'request' can be accessed in the clean() 
	# function.
	def __init__(self, *args, **kwargs):
		self.request = kwargs.pop('request', None)
		super(OperationHistoryForm, self).__init__(*args, **kwargs)

	# Override clean so forms can be saved without validating (so data 
	# isn't lost if the form can't be completed), but still raises 
	# exceptions when form is done incorrectly.
	def clean(self):
		msg = "Este campo es obligatorio."
		cleaned_data = super(OperationHistoryForm, self).clean()

		# On validation ('submit' in request), checks if signature 
		# forms fields are filled out and raises exceptions on any 
		# fields left blank.
		if (self.request.POST):
			if ('submit' in self.request.POST):
				institution = cleaned_data.get('institution')
				if (institution == ''):
					self.add_error('institution', msg)
				
				preop_diagnosis = cleaned_data.get('preop_diagnosis')
				if (preop_diagnosis == ''):
					self.add_error('preop_diagnosis', msg)
				
				intervention = cleaned_data.get('intervention')
				if (intervention == ''):
					self.add_error('intervention', msg)
				
				postop_diagnosis = cleaned_data.get('postop_diagnosis')
				if (postop_diagnosis == ''):
					self.add_error('postop_diagnosis', msg)

				follow_up = cleaned_data.get('follow_up')
				if (follow_up == ''):
					self.add_error('follow_up', msg)


