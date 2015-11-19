# coding=utf-8

import datetime
import uuid

from django.contrib.auth.models import User
from django.db import models

from django import forms

from django.forms import ModelForm
from django.forms import PasswordInput
from django.forms import EmailInput
from django.forms import CheckboxInput

from Residence import Residence

"""Dummy model for Users. No information will be stored in this model, it's just being used to create Users. Not a necessary model, but makes the user creation in profile.py much simpler. User permissions used in this app are also created in this model.
"""
class Profile(models.Model):
	uuid = models.CharField(max_length=200, unique=True, default=uuid.uuid4)
	first_name = models.CharField(max_length=30, blank=True, null=True)
	last_name = models.CharField(max_length=30, blank=True, null=True)
	username = models.CharField(max_length=30, unique=True)
	password = models.CharField(max_length=200)
	cpassword = models.CharField(max_length=200)
	email = models.CharField(max_length=200, unique=True)
	is_staff = models.BooleanField(default=True)
	is_active = models.BooleanField(default=True)
	add_users = models.BooleanField(default=False)
	delete_info = models.BooleanField(default=False)
	restrict_to_home = models.BooleanField(default=True)
	homes = models.ForeignKey(Residence, blank=True, null=True)
	add_edit_forms = models.BooleanField(default=False)
	view = models.BooleanField(default=True)
	show_only =  models.BooleanField(default=False)
	last_saved = models.DateTimeField(blank=True, null=True)

	# Meta class defines database table and labels, and clears any default permissions.
	class Meta:
		app_label = 'tracker'
		db_table = 'tracker_profile'
		default_permissions = ()

		# Permissions used by users in this app
		permissions = (
			('add_users', 'Add Users'),
			('delete_info', 'Delete Info'),
			('add_edit_forms', 'Add and Edit Forms'),
			('view', 'View'),
			('restrict_to_home', 'Restrict to Home'),
			('show-only', 'Show Only'),
		)


"""Form for the Profile model."""
class ProfileForm(ModelForm):

	# Meta class defines the fields and Spanish labels for the form. Also defines any widgets being used.
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
			'add_users',
			'delete_info',
			'add_edit_forms',
			'view',
			'restrict_to_home',
			'homes',
			'show_only',
		)
		labels = {
			'first_name': 'Nombre',
			'last_name': 'Apellido',
			'username': 'Nombre de Usario',
			'password': 'Contraseña',
			'cpassword': 'Confirmar Contraseña',
			'email': 'Correo Electrónico',
			'is_staff': '¿Es el personal?',
			'add_users': 'Añadir Otros Usuarios',
			'delete_info': 'Eliminar Información',
			'add_edit_forms': 'Añadir y Editar Formas',
			'view': 'Ver',
		}
		widgets = {
			'password': PasswordInput(),
			'email': EmailInput(),
			'cpassword': PasswordInput(),
			'is_staff': CheckboxInput(),
			'add_users': CheckboxInput(),
			'delete_info': CheckboxInput(),
			'add_edit_forms': CheckboxInput(),
			'view': CheckboxInput(),
		}

	# Override __init__ so 'request' can be accessed in the clean() function.
	def __init__(self, *args, **kwargs):
		self.request = kwargs.pop('request', None)
		super(ProfileForm, self).__init__(*args, **kwargs)

	# Override clean so forms can be saved without validating (so data isn't lost if the form can't be completed), but still raises exceptions when form is done incorrectly.
	def clean(self):
		msg = "Este campo es obligatorio." #Validation exception message
		cleaned_data = super(ProfileForm, self).clean()

		# On validation ('submit' in request), checks if signature forms fields are filled out and raises exceptions on any fields left blank.
		if self.request.method=='POST':
			if 'submit' in self.request.POST:

				# Checks that username is unique.
				usernames = User.objects.values_list('username', flat=True)
				username = cleaned_data.get('username')
				if username in usernames:
					self.add_error('username', 'Nombre de usuario debe ser único.')

				# Checks that password and confirm password match.
				password = cleaned_data.get('password')
				cpassword = cleaned_data.get('cpassword')
				if password != cpassword:
					self.add_error('password', 'La contraseña no coincide.')

				# Checks that email is unique.
				emails = User.objects.values_list('email', flat=True)
				email = cleaned_data.get('email')
				if email in emails:
					self.add_error('email', 'Este correo electrónico ya tiene una cuenta.')

				#Checks that view is selected for all non-show-only users.
				view = cleaned_data.get('view')
				show_only = cleaned_data.get('view')
				if view is False and show_only is False:
					self.add_errors('view', 'El usuario debe ser capaz de ver la información.')

				# Checks that no other permissions have been selected for show-only users.
				add_users = cleaned_data.get('add_users')
				delete_info = cleaned_data.get('delete_info')
				add_edit_forms = cleaned_data.get('add_edit_forms')
				if show_only is True:
					if view or add_users or delete_info or add_edit_forms or restrict_to_homes:
						self.add_errors('show_only', 'No hay otros permisos se pueden añadir en presentas solamente.')

				# Checks that a home is selected for any user restricted to a home.
				restrict_to_home = cleaned_data.get('restrict_to_home')
				homes = cleaned_data.get('homes')
				if restrict_to_homes and homes is None:
					self.add_errors('show_only', 'Se ha seleccionado ningún hogar.')										


"""Extra information to be saved for the user, including UUID and home-restriction, if applicable.
"""
class UserUUID(models.Model):
	user = models.OneToOneField(User)
	uuid = models.CharField(max_length=200, unique=True, default=uuid.uuid4)
	home = models.ForeignKey(Residence, blank=True, null=True)

	class Meta:
		app_label = 'tracker'
		db_table = 'tracker_useruuid'
		default_permissions = ()









