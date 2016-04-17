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
	explanation = forms.CharField(label="Explique su problema:", 
		widget=forms.Textarea, max_length=10000, required=False)

