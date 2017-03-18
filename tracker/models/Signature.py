# coding=utf-8

from django import forms


"""The form for the signature. Attached at the end of every exam form.
"""

class SignatureForm(forms.Form):
    signature_name = forms.CharField(max_length=30, required=False,
                                     label='Nombres')
    signature_surname = forms.CharField(max_length=30, required=False,
                                        label='Apellidos')
    signature_emp = forms.CharField(max_length=30, required=False,
                                    label='EMP')
    signature_direction = forms.CharField(max_length=30, required=False,
                                          label='Direccion')
    signature_cell = forms.CharField(max_length=30, required=False,
                                     label='Celular')

    # Override __init__ so 'request' can be accessed in the clean()
    # function.
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(SignatureForm, self).__init__(*args, **kwargs)

    # Override clean so forms can be saved without validating (so data
    # isn't lost if the form can't be completed), but still raises
    # exceptions when form is done incorrectly.
    def clean(self):
        msg = "Este campo es obligatorio."  # Validation exception message
        cleaned_data = super(SignatureForm, self).clean()

        # On validation ('submit' in request), checks if signature
        # forms fields are filled out and raises exceptions on any
        # fields left blank.
        if (self.request.POST):
            if ('submit' in self.request.POST):

                signature_name = cleaned_data.get('signature_name')
                if (signature_name == ''):
                    self.add_error('signature_name', msg)

                signature_surname = cleaned_data.get('signature_surname')
                if (signature_surname == ''):
                    self.add_error('signature_surname', msg)

                signature_emp = cleaned_data.get('signature_emp')
                if (signature_emp == ''):
                    self.add_error('signature_emp', msg)

                signature_direction = cleaned_data.get('signature_direction')
                if (signature_direction == ''):
                    self.add_error('signature_direction', msg)

                signature_cell = cleaned_data.get('signature_cell')
                if (signature_cell == ''):
                    self.add_error('signature_cell', msg)
