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


"""Form to populate the User model and the UserUUID model (extra info 
for user), including permissions.
"""
class ProfileForm(forms.Form):
	first_name = forms.CharField(max_length=30, 
								 required=False, 
								 label='Nombre')
	last_name = forms.CharField(max_length=30, 
							    required=False, 
							    label='Apellido')
	username = forms.CharField(max_length=30, label='Nombre de Usario')
	password = forms.CharField(max_length=200, 
							   label='Contraseña', 
							   widget=forms.PasswordInput)
	cpassword = forms.CharField(max_length=200, 
								label='Confirmar Contraseña', 
								widget=forms.PasswordInput)
	email = forms.EmailField(max_length=200, label='Correo Electrónico')
	is_staff = forms.BooleanField(initial=True, 
								  required=False, 
								  label='¿Es el personal?',
								  widget=forms.CheckboxInput)
	add_users = forms.BooleanField(initial=False, 
								   required=False, 
								   label='Añadir Otros Usuarios', 
								   widget=forms.CheckboxInput)
	delete_info = forms.BooleanField(initial=False, 
									 required=False, 
									 label='Eliminar Información', 
									 widget=forms.CheckboxInput)
	restrict_to_home = forms.BooleanField(initial=True, 
										  required=False, 
										  label='Restringir a Casa', 
										  widget=forms.CheckboxInput)
	home = forms.ModelChoiceField(queryset=Residence.objects.all(), 
								  required=False, 
								  label='Casa')
	add_edit_forms = forms.BooleanField(initial=False, 
										required=False, 
										label='Añadir y Editar Formas', 
										widget=forms.CheckboxInput)
	view = forms.BooleanField(initial=True, 
							  required=False, 
							  label='Ver', 
							  widget=forms.CheckboxInput)
	show_only = forms.BooleanField(initial=False, 
								   required=False, 
								   label='Monstrar Solo', 
								   widget=forms.CheckboxInput)

	# Override __init__ so 'request' can be accessed in the clean() 
	# function.
	def __init__(self, *args, **kwargs):
		self.request = kwargs.pop('request', None)
		super(ProfileForm, self).__init__(*args, **kwargs)

	# Override clean so forms can be saved without validating (so data
	# isn't lost if the form can't be completed), but still raises 
	# exceptions when form is done incorrectly.
	def clean(self):
		msg = "Este campo es obligatorio." #Validation exception message
		cleaned_data = super(ProfileForm, self).clean()

		# On validation ('submit' in request), checks if signature 
		# forms fields are filled out and raises exceptions on any 
		# fields left blank.
		if (self.request.POST):
			if ('submit' in self.request.POST):

				# Checks that username is unique.
				usernames = User.objects.values_list('username', flat=True)
				username = cleaned_data.get('username')
				if (username in usernames):
					self.add_error('username', 'Nombre de usuario debe ser '
					'único.')

				# Checks that password and confirm_password match.
				password = cleaned_data.get('password')
				cpassword = cleaned_data.get('cpassword')
				if (password != cpassword):
					self.add_error('password', 'La contraseña no coincide.')

				# Checks that email is unique.
				emails = User.objects.values_list('email', flat=True)
				email = cleaned_data.get('email')
				if (email in emails):
					self.add_error('email', 'Este correo electrónico ya ' 
						'tiene una cuenta.')


				view = cleaned_data.get('view')
				if view is not True:
					view = False
				show_only = cleaned_data.get('show_only')
				if show_only is not True:
					show_only = False
				add_edit_forms= cleaned_data.get('add_edit_forms')
				if add_edit_forms is not True:
					add_edit_forms = False
				delete_info = cleaned_data.get('delete_info')
				if delete_info is not True:
					delete_info = False
				add_users = cleaned_data.get('add_users')
				if add_users is not True:
					add_users = False
				restrict_to_home = cleaned_data.get('restrict_to_home')
				if restrict_to_home is not True:
					restrict_to_home = False

				# Checks that view is selected for all non-show-only 
				# users.
				view = cleaned_data.get('view')
				show_only = cleaned_data.get('show_only')
				if (view is False and show_only is False):
					self.add_error('view', 'El usuario debe ser capaz de ver '
						'la información.')

				# Checks that no other permissions have been selected 
				# for show-only users.
				add_users = cleaned_data.get('add_users')
				delete_info = cleaned_data.get('delete_info')
				add_edit_forms = cleaned_data.get('add_edit_forms')
				if (show_only is True):
					if (view or add_users or delete_info or add_edit_forms or restrict_to_home):
						self.add_error('show_only', 'No hay otros permisos ' 
							'se pueden añadir en presentas solamente.')

				# Checks that a home is selected for any user 
				# restricted to a home.
				restrict_to_home = cleaned_data.get('restrict_to_home')
				home = cleaned_data.get('home')
				if (restrict_to_home and home is None):
					self.add_error('restrict_to_home', 'Se ha seleccionado ningún '
						'hogar.')


"""Form to edit the name of a user in the User model. The clean() 
method checks the password for security.
"""
class EditNameForm(forms.Form):
	first_name = forms.CharField(max_length=30, required=False, 
		label='Nombre')
	last_name = forms.CharField(max_length=30, required=False, 
		label='Apellido')
	password = forms.CharField(max_length=200, label='Contraseña', 
		widget=forms.PasswordInput)

	# Override __init__ so 'request' can be accessed in the clean() 
	# function.
	def __init__(self, *args, **kwargs):
		self.request = kwargs.pop('request', None)
		super(EditNameForm, self).__init__(*args, **kwargs)

	# Override clean so forms can be saved without validating (so data
	# isn't lost if the form can't be completed), but still raises 
	# exceptions when form is done incorrectly.
	def clean(self):
		msg = "Este campo es obligatorio." #Validation exception message
		cleaned_data = super(EditNameForm, self).clean()

		# On validation ('submit' in request), checks if signature 
		# forms fields are filled out and raises exceptions on any 
		# fields left blank.
		if (self.request.POST):
			password = cleaned_data.get('password')
			if (not self.request.user.check_password(password)):
				self.add_error('password', 'Tu contraseña es incorrecta.')
				print self._errors


"""Form to edit the email of a user in the User model. The clean() 
method checks the password for security.
"""
class EditEmailForm(forms.Form):
	email = forms.EmailField(max_length=200, label='Correo Electrónico')
	password = forms.CharField(max_length=200, label='Contraseña', 
		widget=forms.PasswordInput)

	# Override __init__ so 'request' can be accessed in the clean() 
	# function.
	def __init__(self, *args, **kwargs):
		self.request = kwargs.pop('request', None)
		super(EditEmailForm, self).__init__(*args, **kwargs)

	# Override clean so forms can be saved without validating (so data
	# isn't lost if the form can't be completed), but still raises 
	# exceptions when form is done incorrectly.
	def clean(self):
		msg = "Este campo es obligatorio." #Validation exception message
		cleaned_data = super(EditEmailForm, self).clean()

		# On validation ('submit' in request), checks if password 
		# forms fields are filled out and raises exceptions on any 
		# fields left blank.
		if (self.request.POST):
			password = cleaned_data.get('password')
			if (not self.request.user.check_password(password)):
				self.add_error('password', 'Tu contraseña es incorrecta.')


"""Form to edit the password of a user in the User model. The clean() 
method checks the password for security.
"""
class EditPasswordForm(forms.Form):
	old_password = forms.CharField(max_length=200, label='Contraseña', 
		widget=forms.PasswordInput)
	password = forms.CharField(max_length=200, label='Contraseña', 
		widget=forms.PasswordInput)
	cpassword = forms.CharField(max_length=200, label='Confirmar Contraseña', 
		widget=forms.PasswordInput)

	# Override __init__ so 'request' can be accessed in the clean() 
	# function.
	def __init__(self, *args, **kwargs):
		self.request = kwargs.pop('request', None)
		super(EditPasswordForm, self).__init__(*args, **kwargs)

	# Override clean so forms can be saved without validating (so data
	# isn't lost if the form can't be completed), but still raises 
	# exceptions when form is done incorrectly.
	def clean(self):
		msg = "Este campo es obligatorio." #Validation exception message
		cleaned_data = super(EditPasswordForm, self).clean()

		# On validation ('submit' in request), checks if signature 
		# forms fields are filled out and raises exceptions on any 
		# fields left blank.
		if (self.request.POST):
			old_password = cleaned_data.get('old_password')
			if (self.request.user.check_password(old_password)):
				password = cleaned_data.get('password')
				cpassword = cleaned_data.get('cpassword')
				if password == '':
					self.add_error('password', 'Por favor, añada una '
						'nueva contraseña.')
				elif cpassword == '':
					self.add_error('password', 'Por favor, confirme su '
						'nueva contraseña.')
				else:
					if (password != cpassword):
						self.add_error('password', 'Sus nuevas '
							'contraseñas no coinciden.')
			else:
				self.add_error('password', 'Tu contraseña es incorrecta.')


"""Form to edit the staff status of a user in the User model. The 
clean() method checks the password for security.
"""
class EditIsStaffForm(forms.Form):
	is_staff = forms.BooleanField(required=False, label='¿Es el personal?', widget=forms.CheckboxInput)
	password = forms.CharField(max_length=200, label='Contraseña', 
		widget=forms.PasswordInput)

	# Override __init__ so 'request' can be accessed in the clean() 
	# function.
	def __init__(self, *args, **kwargs):
		self.request = kwargs.pop('request', None)
		super(EditIsStaffForm, self).__init__(*args, **kwargs)

	# Override clean so forms can be saved without validating (so data
	# isn't lost if the form can't be completed), but still raises 
	# exceptions when form is done incorrectly.
	def clean(self):
		msg = "Este campo es obligatorio." #Validation exception message
		cleaned_data = super(EditIsStaffForm, self).clean()

		# On validation ('submit' in request), checks if signature 
		# forms fields are filled out and raises exceptions on any 
		# fields left blank.
		if (self.request.POST):
			password = cleaned_data.get('password')
			if (not self.request.user.check_password(password)):
				self.add_error('password', 'Tu contraseña es incorrecta.')


"""Form to edit the active status of a user in the User model. The 
clean() method checks the password for security.
"""
class EditIsActiveForm(forms.Form):
	is_active = forms.BooleanField(required=False, label='¿Es activo?', 
		widget=forms.CheckboxInput)
	password = forms.CharField(max_length=200, label='Contraseña', 
		widget=forms.PasswordInput)

	# Override __init__ so 'request' can be accessed in the clean() 
	# function.
	def __init__(self, *args, **kwargs):
		self.request = kwargs.pop('request', None)
		super(EditIsActiveForm, self).__init__(*args, **kwargs)

	# Override clean so forms can be saved without validating (so data
	# isn't lost if the form can't be completed), but still raises 
	# exceptions when form is done incorrectly.
	def clean(self):
		msg = "Este campo es obligatorio." #Validation exception message
		cleaned_data = super(EditIsActiveForm, self).clean()

		# On validation ('submit' in request), checks if signature 
		# forms fields are filled out and raises exceptions on any 
		# fields left blank.
		if (self.request.POST):
			password = cleaned_data.get('password')
			if (not self.request.user.check_password(password)):
				self.add_error('password', 'Tu contraseña es incorrecta.')


"""Form to edit the permissions of a user in the User model. This form 
edits their ability to add users. The clean() method checks the 
password for security.
"""
class EditAddUsersForm(forms.Form):
	add_users = forms.BooleanField(required=False, 
								   label='Añadir Otros Usuarios', 
								   widget=forms.CheckboxInput)
	password = forms.CharField(max_length=200, label='Contraseña', 
		widget=forms.PasswordInput)

	# Override __init__ so 'request' can be accessed in the clean() 
	# function.
	def __init__(self, *args, **kwargs):
		self.request = kwargs.pop('request', None)
		super(EditAddUsersForm, self).__init__(*args, **kwargs)

	# Override clean so forms can be saved without validating (so data
	# isn't lost if the form can't be completed), but still raises 
	# exceptions when form is done incorrectly.
	def clean(self):
		msg = "Este campo es obligatorio." #Validation exception message
		cleaned_data = super(EditAddUsersForm, self).clean()

		# On validation ('submit' in request), checks if signature 
		# forms fields are filled out and raises exceptions on any 
		# fields left blank.
		if (self.request.POST):
			password = cleaned_data.get('password')
			if (not self.request.user.check_password(password)):
				self.add_error('password', 'Tu contraseña es incorrecta.')


"""Form to edit the permissions of a user in the User model. This form 
edits their ability to delete information. The clean() method checks 
the password for security.
"""
class EditDeleteInfoForm(forms.Form):
	delete_info = forms.BooleanField(required=False, 
									 label='Eliminar Información', 
									 widget=forms.CheckboxInput)
	password = forms.CharField(max_length=200, label='Contraseña', 
		widget=forms.PasswordInput)

	# Override __init__ so 'request' can be accessed in the clean() 
	# function.
	def __init__(self, *args, **kwargs):
		self.request = kwargs.pop('request', None)
		super(EditDeleteInfoForm, self).__init__(*args, **kwargs)

	# Override clean so forms can be saved without validating (so data
	# isn't lost if the form can't be completed), but still raises 
	# exceptions when form is done incorrectly.
	def clean(self):
		msg = "Este campo es obligatorio." #Validation exception message
		cleaned_data = super(EditDeleteInfoForm, self).clean()

		# On validation ('submit' in request), checks if signature 
		# forms fields are filled out and raises exceptions on any 
		# fields left blank.
		if (self.request.POST):
			password = cleaned_data.get('password')
			if (not self.request.user.check_password(password)):
				self.add_error('password', 'Tu contraseña es incorrecta.')


"""Form to edit the permissions of a user in the User model. This form 
edits their ability to add and edit forms. The clean() method checks 
the password for security.
"""
class EditAddEditFormsForm(forms.Form):
	add_edit_forms = forms.BooleanField(required=False, 
										label='Añadir y Editar Formas', 
										widget=forms.CheckboxInput)
	password = forms.CharField(max_length=200, label='Contraseña', 
		widget=forms.PasswordInput)

	# Override __init__ so 'request' can be accessed in the clean() 
	# function.
	def __init__(self, *args, **kwargs):
		self.request = kwargs.pop('request', None)
		super(EditAddEditFormsForm, self).__init__(*args, **kwargs)

	# Override clean so forms can be saved without validating (so data
	# isn't lost if the form can't be completed), but still raises 
	# exceptions when form is done incorrectly.
	def clean(self):
		msg = "Este campo es obligatorio." #Validation exception message
		cleaned_data = super(EditAddEditFormsForm, self).clean()

		# On validation ('submit' in request), checks if signature 
		# forms fields are filled out and raises exceptions on any 
		# fields left blank.
		if (self.request.POST):
			password = cleaned_data.get('password')
			if (not self.request.user.check_password(password)):
				self.add_error('password', 'Tu contraseña es incorrecta.')


"""Form to edit the permissions of a user in the User model. This form 
edits whether the user is show only (removes identifying material). 
The clean() method checks the password for security.
"""
class EditShowOnlyForm(forms.Form):
	show_only = forms.BooleanField(required=False, label='Añadir Otros Usuarios', widget=forms.CheckboxInput)
	password = forms.CharField(max_length=200, label='Contraseña', widget=forms.PasswordInput)

	# Override __init__ so 'request' can be accessed in the clean() 
	# function.
	def __init__(self, *args, **kwargs):
		self.request = kwargs.pop('request', None)
		super(EditShowOnlyForm, self).__init__(*args, **kwargs)

	# Override clean so forms can be saved without validating (so data
	# isn't lost if the form can't be completed), but still raises 
	# exceptions when form is done incorrectly.
	def clean(self):
		msg = "Este campo es obligatorio." #Validation exception message
		cleaned_data = super(EditShowOnlyForm, self).clean()

		# On validation ('submit' in request), checks if signature 
		# forms fields are filled out and raises exceptions on any 
		# fields left blank.
		if (self.request.POST):
			password = cleaned_data.get('password')
			if (not self.request.user.check_password(password)):
				self.add_error('password', 'Tu contraseña es incorrecta.')


"""Form to edit the permissions of a user in the User model. This form 
edits whether they're restricted to their home and, if so, which home. 
The clean() method checks the password for security.
"""
class EditRestrictToHomeForm(forms.Form):
	restrict_to_home = forms.BooleanField(required=False, 
										  label='Añadir Otros Usuarios', 
										  widget=forms.CheckboxInput)
	home = forms.ModelChoiceField(queryset=Residence.objects.all(), 
								  required=False, 
								  label='Casa')
	password = forms.CharField(max_length=200, label='Contraseña', 
		widget=forms.PasswordInput)

	# Override __init__ so 'request' can be accessed in the clean() 
	# function.
	def __init__(self, *args, **kwargs):
		self.request = kwargs.pop('request', None)
		super(EditRestrictToHomeForm, self).__init__(*args, **kwargs)

	# Override clean so forms can be saved without validating (so data
	# isn't lost if the form can't be completed), but still raises 
	# exceptions when form is done incorrectly.
	def clean(self):
		msg = "Este campo es obligatorio." #Validation exception message
		cleaned_data = super(EditRestrictToHomeForm, self).clean()

		# On validation ('submit' in request), checks if signature 
		# forms fields are filled out and raises exceptions on any 
		# fields left blank.
		if (self.request.POST):
			password = cleaned_data.get('password')
			if (self.request.user.check_password(password)):
				restrict_to_home = cleaned_data.get('restrict_to_home')
				home = cleaned_data.get('home')
				if (restrict_to_home and home is None):
					self.add_error('home', 'Por favor elige una casa.')
				elif (not restrict_to_home and home is not None):
					self.add_error('home', 'No seleccione un hogar como '
						'usuario no se limita a casa.')
			else:
				self.add_error('password', 'Tu contraseña es incorrecta.')


"""Extra information to be saved for the user, including UUID and home-
restriction, if applicable. All fields will be populated by the 
ProfileForm, after the User has been created.
"""
class UserUUID(models.Model):
	user = models.OneToOneField(User)
	uuid = models.CharField(max_length=200, unique=True, default=uuid.uuid4)
	home = models.ForeignKey(Residence, blank=True, null=True)
	# For de-duping forms that have been edited.
	last_saved = models.DateTimeField()

	# Meta class defines database table and labels, and clears any 
	# default permissions.
	class Meta:
		app_label = 'tracker'
		db_table = 'tracker_useruuid'
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



