import datetime

from django.db import models
from django.forms import ModelForm

class Signature(models.Model):
    name = models.CharField(max_length=200, blank=True, null=True)
    surname = models.CharField(max_length=200, blank=True, null=True)
    emp = models.CharField(max_length=200, blank=True, null=True)
    direction = models.CharField(max_length=200, blank=True, null=True)
    cell = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        app_label = 'tracker'
        db_table = 'tracker_signature'

    def __unicode__(self):
        return self.name

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
            'direction': 'Direccion',
            'cell': 'Celular',
        }

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(SignatureForm, self).__init__(*args, **kwargs)

    def clean(self):
        msg = "This field is required."
        cleaned_data = super(SignatureForm, self).clean()

        if self.request.method == 'POST':
            name = cleaned_data.get('name')
            surname = cleaned_data.get('surname')
            emp = cleaned_data.get('emp')
            direction = cleaned_data.get('direction')
            cell = cleaned_data.get('cell')
            if 'submit' in self.request.POST:
                if name=='':
                    self.add_error('name', msg)
                if surname=='':
                    self.add_error('surname', msg)
                if emp=='':
                    self.add_error('emp', msg)
                if direction=='':
                    self.add_error('direction', msg)
                if cell=='':
                    self.add_error('cell', msg)


