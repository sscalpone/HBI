# coding=utf-8

import datetime
import uuid

from django.contrib.auth.models import User
from django.db import models
from django.forms import ModelForm
from django.forms import DateInput

from Child import Child


"""Model for Disease History, which records a child's disease history. 
This model references the Signature model and the Child model. All 
fields are allowed to be saved null so that forms can be saved before 
validation to prevent losing information if the form can't be 
completed. This is overriden in the clean() method.
"""
class DiseaseHistory(models.Model):
	uuid = models.CharField(max_length=200, unique=True, default=uuid.uuid4)
	child = models.ForeignKey(Child, blank=True, null=True)
	date = models.DateField(default=datetime.date.today)
	institution = models.CharField(max_length=200, null=True, blank=True)
	diagnosis = models.TextField(null=True, blank=True)
	studies = models.TextField(null=True, blank=True)
	treatment = models.TextField(null=True, blank=True)
	signature_name = models.CharField(max_length=200, blank=True, null=True)
	signature_surname = models.CharField(max_length=200, blank=True, 
		null=True)
	signature_emp = models.CharField(max_length=200, blank=True, null=True)
	signature_direction = models.CharField(max_length=200, blank=True, 
		null=True)
	signature_cell = models.CharField(max_length=200, blank=True, null=True)
	# For de-duping forms that have been edited.
	last_saved = models.DateTimeField(default=datetime.datetime.utcnow) 

	# Meta class defines database table and labels, and clears any 
	# default permissions.
	class Meta:
		app_label='tracker'
		db_table='tracker_diseasehistory'
		default_permissions = ()


"""The form for the Disease History model."""
class DiseaseHistoryForm(ModelForm):
	
	# Meta class defines the fields and Spanish labels for the form.
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
		widgets = {
			'date': DateInput(attrs={'placeholder': 'DD/MM/AAAA', 'format': 'DD/MM/AAAA'}),
		}

	# Override __init__ so 'request' can be accessed in the clean() 
	# function.
	def __init__(self, *args, **kwargs):
		self.request = kwargs.pop('request', None)
		super(DiseaseHistoryForm, self).__init__(*args, **kwargs)

	# Override clean so forms can be saved without validating (so data 
	# isn't lost if the form can't be completed), but still raises 
	# exceptions when form is done incorrectly.
	def clean(self):
		msg = "Este campo es obligatorio."
		cleaned_data = super(DiseaseHistoryForm, self).clean()
		
		# On validation ('submit' in request), checks if signature 
		# forms fields are filled out and raises exceptions on any 
		# fields left blank.
		if (self.request.POST):
			if ('submit' in self.request.POST):
				
				institution = cleaned_data.get('institution')
				if (institution == ''):
					self.add_error('institution', msg)
				
				diagnosis = cleaned_data.get('diagnosis')
				if (diagnosis == ''):
					self.add_error('diagnosis', msg)
				
				studies = cleaned_data.get('studies')
				if (studies == ''):
					self.add_error('studies', msg)
				
				treatment = cleaned_data.get('treatment')
				if (treatment == ''):
					self.add_error('treatment', msg)







