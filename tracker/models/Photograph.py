# coding=utf-8

import datetime
import uuid

from django.contrib.auth.models import User
from django.db import models
from django.forms import ModelForm
from django.forms import RadioSelect

from Child import Child

class Photograph(models.Model):
	uuid = models.CharField(max_length=200, unique=True, default=uuid.uuid4)
	child = models.ForeignKey(Child)
	date = models.DateField()
	photo = models.ImageField(upload_to='photos', blank=True, null=True)
	last_saved = models.DateTimeField()

	class Meta:
		app_label = 'tracker'
		db_table = 'tracker_photograph'
		default_permissions = ()


class PhotographForm(ModelForm):
	class Meta:
		model = Photograph
		fields = (
			'date',
			'photo'
		)
		labels = {
			'date': 'Fecha',
			'photo': 'Fotografía'
		}

	def __init__(self, *args, **kwargs):
		self.request = kwargs.pop('request', None)
		super(PhotographForm, self).__init__(*args, **kwargs)

	def clean(self):
		msg = "Este campo es obligatorio."
		cleaned_data = super(PhotographForm, self).clean()

		if self.request.POST:
			if 'submit' in self.request.POST:
				photo = cleaned_data.get('photo')
				if photo is None:
					self.add_error('photo', msg)






