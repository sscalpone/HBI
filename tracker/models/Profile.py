# coding=utf-8

from django.contrib.auth.models import User
from django.db import models
from django.forms import ModelForm

from django.forms import PasswordInput
from django.forms import EmailInput
from django.forms import CheckboxInput

from ProfilePermissions import ProfilePermissions


class Profile(models.Model):
	first_name = models.CharField(max_length=30, blank=True, null=True)
	last_name = models.CharField(max_length=30, blank=True, null=True)
	username = models.CharField(max_length=30)
	password = models.CharField(max_length=200)
	cpassword = models.CharField(max_length=200)
	email = models.CharField(max_length=200)
	is_staff = models.BooleanField(default=True)
	is_active = models.BooleanField(default=True)
	permission = models.ForeignKey(ProfilePermissions)

	class Meta:
		app_label = 'tracker'
		db_table = 'tracker_profile'

		permissions = (
			('add_users', 'Add Users'),
			('delete_info', 'Delete Info'),
			('add_edit_forms', 'Add and Edit Forms'),
			('view', 'View'),
		)


class ProfileForm(ModelForm):
	class Meta:
		model = Profile
		exclude = (
			'is_active',
		)
		fields = (
			'first_name',
			'last_name',
			'username',
			'password',
			'cpassword',
			'email',
			'is_staff',
		)
		labels = {
			'first_name': 'Nombre',
			'last_name': 'Apellido',
			'username': 'Nombre de Usario',
			'password': 'Contraseña',
			'cpassword': 'Confirmar Contraseña',
			'email': 'Correo Electrónico',
			'is_staff': '¿Es el personal?',
		}
		widgets = {
			'password': PasswordInput(),
			'email': EmailInput(),
			'cpassword': PasswordInput(),
			'is_staff': CheckboxInput(),
		}


	def __init__(self, *args, **kwargs):
		self.request = kwargs.pop('request', None)
		super(ProfileForm, self).__init__(*args, **kwargs)

	def clean(self):
		msg = "Este campo es obligatorio."
		cleaned_data = super(ProfileForm, self).clean()

		if self.request.method=='POST':
			if 'submit' in self.request.POST:
				usernames = User.objects.values_list('username', flat=True)
				username = cleaned_data.get('username')
				if username in usernames:
					self.add_error('username', 'Nombre de usuario debe ser único.')

				password = cleaned_data.get('password')
				cpassword = cleaned_data.get('cpassword')
				if password != cpassword:
					self.add_error('password', 'La contraseña no coincide.')

				emails = User.objects.values_list('email', flat=True)
				email = cleaned_data.get('email')
				if email in emails:
					self.add_error('email', 'Este correo electrónico ya tiene una cuenta.')


class EditProfileForm(ModelForm):
	class Meta:
		model = Profile
		exclude = (
			'password',
			'cpassword',
			'is_staff',
			'is_active',
		)
		fields = (
			'first_name',
			'last_name',
			'username',
			'email',
			'is_staff',
		)
		labels = {
			'first_name': 'Nombre',
			'last_name': 'Apellido',
			'username': 'Nombre de Usario',
			'password': 'Contraseña',
			'cpassword': 'Confirmar Contraseña',
			'email': 'Correo Electrónico',
			'is_staff': '¿Es el personal?',
		}
		widgets = {
			'password': PasswordInput(),
			'email': EmailInput(),
			'cpassword': PasswordInput(),
			'is_staff': CheckboxInput(),
		}


	def __init__(self, *args, **kwargs):
		self.request = kwargs.pop('request', None)
		super(ProfileForm, self).__init__(*args, **kwargs)

	def clean(self):
		msg = "Este campo es obligatorio."
		cleaned_data = super(ProfileForm, self).clean()

		if self.request.method=='POST':
			if 'submit' in self.request.POST:
				usernames = User.objects.values_list('username', flat=True)
				username = cleaned_data.get('username')
				if username in usernames:
					self.add_error('username', 'Nombre de usuario debe ser único.')

				emails = User.objects.values_list('email', flat=True)
				email = cleaned_data.get('email')
				if email in emails:
					self.add_error('email', 'Este correo electrónico ya tiene una cuenta.')



