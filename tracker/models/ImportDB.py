# coding=utf-8

from django import forms


class ImportDBForm(forms.Form):
    upload = forms.FileField(label='Subir')
    fix = forms.BooleanField(initial=False,
                             required=False,
                             label=('Correcta importación anterior (no se '
                                    'recomienda):'),
                             widget=forms.CheckboxInput)
