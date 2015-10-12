# coding=utf-8

import datetime

from django.contrib.auth.models import User
from django.db import models
from django.forms import ModelForm
from django.forms import RadioSelect

from Child import Child
from Signature import Signature

class Documents(models.Model):
	child = models.ForeignKey(Child)
	date = models.DateField()
	title = models.CharField(max_length=200, blank=True, null=True)
	document = models.FileField(upload_to='documents', blank=True, null=True)
	signature = models.ForeignKey(Signature)

class DocumentsForm(ModelForm):
	class Meta:
		model = Documents
		fields = (
			'date',
			'title',
			'document',
		)
		labels = {
			'date': 'Fecha',
			'title': 'Título',
			'document': 'Documento',
		}

	def __init__(self, *args, **kwargs):
		self.request = kwargs.pop('request', None)
		super(DocumentsForm, self).__init__(*args, **kwargs)

	def clean(self):
		msg = "Este campo es obligatorio."
		cleaned_data = super(DocumentsForm, self).clean()

		if self.request.method=='POST':
			if 'submit' in self.request.POST:
				title = cleaned_data.get('title')
				if title=='':
					self.add_error('title', msg)

				document = cleaned_data.get('document')
				if document is None:
					self.add_error('document', msg)


