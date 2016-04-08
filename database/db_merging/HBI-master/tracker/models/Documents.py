# coding=utf-8

import datetime
import uuid

from django.contrib.auth.models import User
from django.db import models
from django.forms import ModelForm
from django.forms import RadioSelect

from Child import Child
from Signature import Signature


"""The Documents model stores any documents users upload about the 
children. It references the Child model and the Signature model. It 
sorts the files into three categories: government, health, and other
documents, which can then be recalled. All fields are allowed to be 
saved null so that forms can be saved before validation to prevent 
losing information if the form can't be completed. This is overriden 
in the clean() method.
"""
class Documents(models.Model):
	# Folder Choices
	GOV = 'Government'
	HEALTH = 'Health'
	OTHER = 'Other'
	FOLDER_CHOICES = (
        (GOV, 'Documentos Gubernamentales'),
        (HEALTH, 'Documentos Salud'),
        (OTHER, 'Otros')
    )

	uuid = models.CharField(max_length=200, unique=True, default=uuid.uuid4)
	child = models.ForeignKey(Child)
	date = models.DateField()
	title = models.CharField(max_length=200, blank=True, null=True)
	document = models.FileField(blank=True, null=True)
	file_to = models.CharField(max_length=10, 
                               choices=FOLDER_CHOICES, 
                               default=HEALTH)
	signature = models.ForeignKey(Signature)
	# For de-duping forms that have been edited.
	last_saved = models.DateTimeField(blank=True, null=True) 

	# Meta class defines database table and labels, and clears any 
	# default permissions.
	class Meta:
		app_label='tracker'
		db_table='tracker_documents'
		default_permissions = ()


"""The form of the Documents model."""
class DocumentsForm(ModelForm):
	
	# Meta class defines the fields and Spanish labels for the form.
	class Meta:
		model = Documents
		
		fields = (
			'date',
			'title',
			'document',
			'file_to',
		)
		
		labels = {
			'date': 'Fecha',
			'title': 'Título',
			'document': 'Documento',
			'file_to': 'Carpeta',
		}

	# Override __init__ so 'request' can be accessed in the clean() 
	# function.
	def __init__(self, *args, **kwargs):
		self.request = kwargs.pop('request', None)
		super(DocumentsForm, self).__init__(*args, **kwargs)

	# Override clean so forms can be saved without validating (so data 
	# isn't lost if the form can't be completed), but still raises 
	# exceptions when form is done incorrectly.
	def clean(self):
		msg = "Este campo es obligatorio."
		cleaned_data = super(DocumentsForm, self).clean()

		# On validation ('submit' in request), checks if signature 
		# forms fields are filled out and raises exceptions on any 
		# fields left blank.
		if (self.request.POST):
			if ('submit' in self.request.POST):
				
				title = cleaned_data.get('title')
				if (title == ''):
					self.add_error('title', msg)

				document = cleaned_data.get('document')
				if (document is None):
					self.add_error('document', msg)


