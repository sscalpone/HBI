# coding=utf-8

from django.contrib.auth.models import User
from django.db import models
from django.forms import ModelForm

from django.forms import CheckboxInput

class ProfilePermissions(models.Model):
	add_users = models.BooleanField(default=False)
	delete_info = models.BooleanField(default=False)
	add_edit_forms = models.BooleanField(default=False)
	view = models.BooleanField(default=True)
	
	class Meta:
		app_label = 'tracker'
		db_table = 'tracker_profilepermissions'


class ProfilePermissionsForm(ModelForm):
	class Meta:
		model = ProfilePermissions
		fields = (
			'add_users',
			'delete_info',
			'add_edit_forms',
			'view',
		)
		labels = {
			'add_users': 'Añadir Otros Usuarios',
			'delete_info': 'Eliminar Información',
			'add_edit_forms': 'Añadir y Editar Formas',
			'view': 'Ver',
		}
		widgets = {
			'add_users': CheckboxInput(),
			'delete_info': CheckboxInput(),
			'add_edit_forms': CheckboxInput(),
			'view': CheckboxInput(),
		}


	def __init__(self, *args, **kwargs):
		self.request = kwargs.pop('request', None)
		super(ProfilePermissionsForm, self).__init__(*args, **kwargs)

	def clean(self):
		msg = "Este campo es obligatorio."
		cleaned_data = super(ProfilePermissionsForm, self).clean()

		view = cleaned_data.get('view')
		if view is False:
			self.add_errors('view', 'El usuario debe ser capaz de ver la información.')



