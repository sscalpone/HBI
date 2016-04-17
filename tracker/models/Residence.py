# coding=utf-8

import datetime
import uuid

from django.contrib.auth.models import User
from django.db import models
from django.forms import ModelForm
from django.forms import DateInput


"""The Residence model saves information about each of the homes the 
children live in. The model is referenced in the Child model. All 
fields are allowed to be saved null so that forms can be saved 
before validation to prevent losing information if the form can't be 
completed. This is overriden in the clean() method.
"""
class Residence(models.Model):
	uuid = models.CharField(max_length=200, unique=True, default=uuid.uuid4)
	residence_name = models.CharField(max_length=200, blank=True, null=True)
	administrator = models.CharField(max_length=200, blank=True, null=True)
	location = models.CharField(max_length=200, blank=True, null=True)
	photo = models.ImageField(upload_to='photos', blank=True, null=True)
	# For de-duping forms that have been edited.
	last_saved = models.DateTimeField(default=datetime.datetime.utcnow)

	# The human-readable version of the model - the residence name.
	def __unicode__(self):
		return self.residence_name

	def get_name(self):
		return self.residence_name

	# Meta class defines database table and labels, and clears any 
	# default permissions.
	class Meta:
		app_label = 'tracker'
		db_table = 'tracker_residence'
		default_permissions = ()


"""The form of the Residence model."""
class ResidenceForm(ModelForm):
	# Meta class defines the fields and Spanish labels for the form. 
	# Also defines any weidgets being used.
	class Meta:
		model = Residence
		
		fields = (
			'residence_name',
			'administrator',
			'location',
			'photo',
		)
		
		labels = {
			'residence_name': 'Casa Girasoles',
			'administrator': 'Administrador',
			'location': 'Localización',
			'photo': 'Fotografía',
		}

	# Override __init__ so 'request' can be accessed in the clean() 
	# function.
	def __init__(self, *args, **kwargs):
		self.request = kwargs.pop('request', None)
		super(ResidenceForm, self).__init__(*args, **kwargs)

	# Override clean so forms can be saved without validating (so data 
	# isn't lost if the form can't be completed), but still raises 
	# exceptions when form is done incorrectly.
	def clean(self):
		msg = "Este campo es obligatorio."
		cleaned_data = super(ResidenceForm, self).clean()

		# On validation ('submit' in request), checks if signature 
		# forms fields are filled out and raises exceptions on any 
		# fields left blank.
		if (self.request.POST):
			if ('submit' in self.request.POST):
				
				residence_name = cleaned_data.get('residence_name')
				if (residence_name == ''):
					self.add_error('residence_name', msg)
				
				location = cleaned_data.get('location')
				if (location == ''):
					self.add_error('location', msg)
				
				administrator = cleaned_data.get('administrator')
				if (administrator == ''):
					self.add_error('administrator', msg)




