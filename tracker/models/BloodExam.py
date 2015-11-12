# coding=utf-8

import datetime
import uuid

from django.contrib.auth.models import User
from django.db import models
from django.forms import ModelForm
from django.forms import RadioSelect

from Child import Child
from Signature import Signature

class BloodExam(models.Model):
    uuid = models.CharField(max_length=200, unique=True, default=uuid.uuid4)
    child = models.ForeignKey(Child)
    date = models.DateField()
    hemoglobin_abnormal = models.BooleanField(default=False)
    hemoglobin_notes = models.TextField(blank=True, null=True)
    elisa_vh1_positive = models.BooleanField(default=False)
    elisa_vh1_notes = models.TextField(blank=True, null=True)
    hepatitis_b_positive = models.BooleanField(default=False)
    hepatitis_b_notes = models.TextField(blank=True, null=True)
    ppd_positive = models.BooleanField(default=False)
    ppd_notes = models.TextField(blank=True, null=True)
    parasites_positive = models.BooleanField(default=False)
    parasites_notes = models.TextField(blank=True, null=True)
    urine_abnormal = models.BooleanField(default=False)
    urine_notes = models.TextField(blank=True, null=True)
    leukocytes_abnormal = models.BooleanField(default=False)
    leukocytes_notes = models.TextField(blank=True, null=True)
    nitrites_abnormal = models.BooleanField(default=False)
    nitrites_notes = models.TextField(blank=True, null=True)
    urobilinogen_abnormal = models.BooleanField(default=False)
    urobilinogen_notes = models.TextField(blank=True, null=True)
    protein_abnormal = models.BooleanField(default=False)
    protein_notes = models.TextField(blank=True, null=True)
    ph_abnormal = models.BooleanField(default=False)
    ph_notes = models.TextField(blank=True, null=True)
    density_abnormal = models.BooleanField(default=False)
    density_notes = models.TextField(blank=True, null=True)
    glucose_abnormal = models.BooleanField(default=False)
    glucose_notes = models.TextField(blank=True, null=True)
    signature = models.ForeignKey(Signature, blank=True, null=True)
    last_saved = models.DateTimeField()

    class Meta:
        app_label = 'tracker'
        db_table = 'tracker_bloodexam'
        default_permissions = ()


class BloodExamForm(ModelForm):
    class Meta:
        model = BloodExam
        fields = (
            'date',
            'hemoglobin_abnormal',
            'hemoglobin_notes',
            'elisa_vh1_positive',
            'elisa_vh1_notes',
            'hepatitis_b_positive',
            'hepatitis_b_notes',
            'ppd_positive',
            'ppd_notes',
            'parasites_positive',
            'parasites_notes',
            'urine_abnormal',
            'urine_notes',
            'urobilinogen_abnormal',
            'urobilinogen_notes',
            'leukocytes_abnormal',
            'leukocytes_notes',
            'nitrites_abnormal',
            'nitrites_notes',
            'urobilinogen_abnormal',
            'urobilinogen_notes',
            'protein_abnormal',
            'protein_notes',
            'ph_abnormal',
            'ph_notes',
            'density_abnormal',
            'density_notes',
            'glucose_abnormal',
            'glucose_notes',
        )
        labels = {
            'date': 'Fecha',
            'hemoglobin_abnormal': 'Hemoglobina',
            'hemoglobin_notes': 'Comentarios',
            'elisa_vh1_positive': 'Elisa VH1',
            'elisa_vh1_notes': 'Comentarios',
            'hepatitis_b_positive': 'Hepatitis B',
            'hepatitis_b_notes': 'Comentarios',
            'ppd_positive': 'PPD',
            'ppd_notes': 'Comentarios', 
            'parasites_positive': 'Parasitos',
            'parasites_notes': 'Comentarios',
            'leukocytes_abnormal': 'Leucocitos',
            'leukocytes_notes': 'Comentarios',
            'nitrites_abnormal': 'Nitritos',
            'nitrites_notes': 'Comentarios',
            'urine_abnormal': 'Orina',
            'urine_notes': 'Comentarios',
            'urobilinogen_abnormal': 'Urobilinogeno',
            'urobilinogen_notes': 'Comentarios',
            'protein_abnormal': 'Proteina',
            'protein_notes': 'Comentarios',
            'ph_abnormal': 'pH',
            'ph_notes': 'Comentarios',
            'density_abnormal': 'Densidad',
            'density_notes': 'Comentarios',
            'glucose_abnormal': 'Glucosa',
            'glucose_notes': 'Comentarios',
        }
        widgets = {
            'hemoglobin_abnormal': RadioSelect(choices=((True, 'Anormal'),(False, 'Normal'))),
            'elisa_vh1_positive': RadioSelect(choices=((True, 'Positivo'),(False, 'Negativo'))),
            'hepatitis_b_positive': RadioSelect(choices=((True, 'Positivo'),(False, 'Negativo'))),
            'ppd_positive': RadioSelect(choices=((True, 'Positivo'),(False, 'Negativo'))),
            'parasites_positive': RadioSelect(choices=((True, 'Positivo'),(False, 'Negativo'))),
            'urine_abnormal': RadioSelect(choices=((True, 'Anormal'),(False, 'Negativo'))),
            'leukocytes_abnormal': RadioSelect(choices=((True, 'Anormal'),(False, 'Normal'))),
            'nitrites_abnormal': RadioSelect(choices=((True, 'Anormal'),(False, 'Normal'))),
            'urobilinogen_abnormal': RadioSelect(choices=((True, 'Anormal'),(False, 'Normal'))),
            'protein_abnormal': RadioSelect(choices=((True, 'Anormal'),(False, 'Normal'))),
            'ph_abnormal': RadioSelect(choices=((True, 'Anormal'),(False, 'Normal'))),
            'density_abnormal': RadioSelect(choices=((True, 'Anormal'),(False, 'Normal'))),
            'glucose_abnormal': RadioSelect(choices=((True, 'Anormal'),(False, 'Normal'))),
        }

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(BloodExamForm, self).__init__(*args, **kwargs)

    def clean(self):
        msg = "Este campo es obligatorio."
        cleaned_data = super(BloodExamForm, self).clean()

        if self.request.method=='POST':
            if 'submit' in self.request.POST:

                hemoglobin_abnormal = cleaned_data.get('hemoglobin_abnormal')
                hemoglobin_notes = cleaned_data.get('hemoglobin_notes')
                if hemoglobin_abnormal and hemoglobin_notes=='':
                    self.add_error('hemoglobin_notes', msg)

                elisa_vh1_positive = cleaned_data.get('elisa_vh1_positive')
                elisa_vh1_notes = cleaned_data.get('elisa_vh1_notes')
                if elisa_vh1_positive and elisa_vh1_notes=='':
                    self.add_error('elisa_vh1_notes', msg)

                hepatitis_b_positive = cleaned_data.get('hepatitis_b_positive')
                hepatitis_b_notes = cleaned_data.get('hepatitis_b_notes')
                if hepatitis_b_positive and hepatitis_b_notes=='':
                    self.add_error('hepatitis_b_notes', msg)

                ppd_positive = cleaned_data.get('ppd_positive')
                ppd_notes = cleaned_data.get('ppd_notes')
                if ppd_positive and ppd_notes=='':
                    self.add_error('ppd_notes', msg)

                parasites_positive = cleaned_data.get('parasites_positive')
                parasites_notes = cleaned_data.get('parasites_notes')
                if parasites_positive and parasites_notes=='':
                    self.add_error('parasites_notes', msg)

                urine_abnormal = cleaned_data.get('urine_abnormal')
                urine_notes = cleaned_data.get('urine_notes')
                if urine_abnormal and urine_notes=='':
                    self.add_error('urine_notes', msg)

                leukocytes_abnormal = cleaned_data.get('leukocytes_abnormal')
                leukocytes_notes = cleaned_data.get('leukocytes_notes')
                if leukocytes_abnormal and leukocytes_notes=='':
                    self.add_error('leukocytes_notes', msg)

                nitrites_abnormal = cleaned_data.get('nitrites_abnormal')
                nitrites_notes = cleaned_data.get('nitrites_notes')
                if nitrites_abnormal and nitrites_notes=='':
                    self.add_error('nitrites_notes', msg)

                urobilinogen_abnormal = cleaned_data.get('urobilinogen_abnormal')
                urobilinogen_notes = cleaned_data.get('urobilinogen_notes')
                if urobilinogen_abnormal and urobilinogen_notes=='':
                    self.add_error('urobilinogen_notes', msg)

                protein_abnormal = cleaned_data.get('protein_abnormal')
                protein_notes = cleaned_data.get('protein_notes')
                if protein_abnormal and protein_notes=='':
                    self.add_error('protein_notes', msg)

                ph_abnormal = cleaned_data.get('ph_abnormal')
                ph_notes = cleaned_data.get('ph_notes')
                if ph_abnormal and ph_notes=='':
                    self.add_error('ph_notes', msg)

                density_abnormal = cleaned_data.get('density_abnormal')
                density_notes = cleaned_data.get('density_notes')
                if density_abnormal and density_notes=='':
                    self.add_error('density_notes', msg)

                glucose_abnormal = cleaned_data.get('glucose_abnormal')
                glucose_notes = cleaned_data.get('glucose_notes')
                if glucose_abnormal and glucose_notes=='':
                    self.add_error('glucose_notes', msg)


