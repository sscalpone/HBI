# coding=utf-8

from django import forms


"""This is the form that is submitted to upload different versions of the
database. This is so the app can be used both on- and offline.
"""

class ImportDBForm(forms.Form):
    upload = forms.FileField(label='Subir')
    fix = forms.BooleanField(initial=False,
                             required=False,
                             label=('Correcta importación anterior (no se '
                                    'recomienda):'),
                             widget=forms.CheckboxInput)
