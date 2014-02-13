# coding=utf-8

from tracker.models import Signature
from django.forms import ModelForm


class SignatureForm(ModelForm):
    class Meta:
        model = Signature
        fields = '__all__'
        labels = {
            'nombres': 'Nombres',
            'apellidos': 'Apellidos',
            'emp': 'EMP',
            'direccion': 'Direction',
            'celular': 'Célular',
        }
