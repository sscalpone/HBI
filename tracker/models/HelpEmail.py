# coding=utf-8

import datetime
import uuid

from django import forms
from django.contrib.auth.models import User

from django.forms import Textarea

from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse

class HelpEmailForm(forms.Form):
	PROBLEM_CHOICES = (
		('EMR Help: Medical Question', 'Tengo una pregunta médica'),
		('EMR Help: Program Question', 
			'Tengo una pregunta sobre este programa'),
	)

	problem = forms.ChoiceField(label="¿Qué tipo de problema?", 
		choices=PROBLEM_CHOICES)
	explanation = forms.CharField(label="Explique su problema:", widget=forms.Textarea, max_length=10000, required=False)

	# # Override __init__ so 'request' can be accessed in the clean() 
	# # function.
	# def __init__(self, *args, **kwargs):
	# 	self.request = kwargs.pop('request', None)
	# 	super(HelpEmailForm, self).__init__(*args, **kwargs)


	# def clean(self):
	# 	cleaned_data = super(HelpEmailForm, self).clean()

	# 	# On validation ('submit' in request), checks if signature 
	# 	# forms fields are filled out and raises exceptions on any 
	# 	# fields left blank.
	# 	if (self.request.POST):
	# 		explanation = cleaned_data.get('explanation')
	# 		if (explanation == ""):
	# 			messages.add_message(request, messages.INFO, 
	# 			'Por favor, explique su problema.')
	# 		return HttpResponseRedirect(reverse('tracker:help'))

