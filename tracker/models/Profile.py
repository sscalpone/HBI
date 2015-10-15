# coding=utf-8

from django.contrib.auth.models import User
from django.db import models
from django.forms import ModelForm

from django.forms import PasswordInput
from django.forms import EmailInput
from django.forms import CheckboxInput

from ProfilePermissions import ProfilePermissions


class Profile(models.Model):
	first_name = models.CharField(max_length=200)
	last_name = models.CharField(max_length=200)
	username = models.CharField(max_length=30)
	password = models.CharField(max_length=200)
	cpassword = models.CharField(max_length=200)
	email = models.CharField(max_length=200)
	permission = models.ForeignKey(ProfilePermissions)

	class Meta:
		app_label = 'tracker'
		db_table = 'tracker_profile'


class ProfileForm(ModelForm):
	class Meta:
		model = Profile
		fields = (
			'first_name',
			'last_name',
			'username',
			'password',
			'cpassword',
			'email',
		)
		labels = {
			'first_name': 'Nombre',
			'last_name': 'Apellido',
			'username': 'Nombre de Usario',
			'password': 'Contraseña',
			'cpassword': 'Confirmar Contraseña',
			'email': 'Correo Electrónico',
		}
		widgets = {
			'password': PasswordInput(),
			'email': EmailInput(),
			'cpassword': PasswordInput(),
		}


	def __init__(self, *args, **kwargs):
		self.request = kwargs.pop('request', None)
		super(ProfileForm, self).__init__(*args, **kwargs)

	def clean(self):
		msg = "Este campo es obligatorio."
		cleaned_data = super(ProfileForm, self).clean()

		if self.request.method=='POST':
			if 'submit' in self.request.POST:
				password = cleaned_data.get('password')
				cpassword = cleaned_data.get('cpassword')
				if password != cpassword:
					self.add_error('password', 'La contraseña no coincide.')




