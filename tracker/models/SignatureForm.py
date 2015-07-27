# coding=utf-8

from tracker.models import Signature
from django.forms import ModelForm

class SignatureForm(ModelForm):
    class Meta:
        model = Signature
        fields = (
            'name',
            'surname',
            'emp',
            'direction',
            'cell',
        )
        labels = {
            'name': 'Nombres',
            'surname': 'Apellidos',
            'emp': 'EMP',
            'direction': 'Dirección',
            'cell': 'Célular',
        }
