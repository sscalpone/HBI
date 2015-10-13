from django.contrib.auth.models import User
from django.db import models
from django.forms import ModelForm


class User(models.Model):
    HIGH = 1
    MEDIUM = 2
    LOW = 3
    PERMISSION_CHOICES = (
        (HIGH, 'Alta Prioridad'),
        (MEDIUM, 'Prioridad Media'),
        (LOW, 'Prioridad Baja')
    )

	username = models.CharField(max_length=30)
	password = models.CharField(max_length=200)
	email = models.Charfield(max_length=200)
	permission = models.IntegerField(choices=PERMISSION_CHOICES, 
                                	 default=LOW)

	class Meta:
        app_label = 'tracker'
        db_table = 'tracker_user'
        verbose_name_plural = "Users"

class UserForm(ModelForm):
	class Meta:
		model = User
		fields= (
			'username',
			'password',
			'email',
		)
		labels = {
			'username': 'Nombre de Usario',
			'password': 'Clave',
			'email': 'Correo Electrónico',
		}
		widgets = {
			'password': PasswordInput(),
			'email': EmailInput()
		}




