import datetime

from Child import Child
from Signature import Signature

from django.db import models

from django.contrib.auth.models import User

from django.core.exceptions import ValidationError

class MedicalExamPart1(models.Model):
    child = models.ForeignKey(Child)
    date = models.DateField()
    background_notes = models.TextField()
    birth_history = models.TextField()
    bcg_vaccine = models.BooleanField(default=False)
    bcg_vaccine_date = models.DateField(blank=True, null=True)
    polio_vaccine = models.BooleanField(default=False)
    polio_vaccine_date = models.DateField(blank=True, null=True)
    dpt_vaccine = models.BooleanField(default=False)
    dpt_vaccine_date = models.DateField(blank=True, null=True)
    hepatitis_b_vaccine = models.BooleanField(default=False)
    hepatitis_b_vaccine_date = models.DateField(blank=True, null=True)
    flu_vaccine = models.BooleanField(default=False)
    flu_vaccine_date = models.DateField(blank=True, null=True)
    yellow_fever_vaccine = models.BooleanField(default=False)
    yellow_fever_vaccine_date = models.DateField(blank=True, null=True)
    spr_vaccine = models.BooleanField(default=False)
    spr_vaccine_date = models.DateField(blank=True, null=True)
    hpv_vaccine = models.BooleanField(default=False)
    hpv_vaccine_date = models.DateField(blank=True, null=True)
    pneumococcal_vaccine = models.BooleanField(default=False)
    pneumococcal_vaccine_date = models.DateField(blank=True, null=True)
    weight = models.FloatField()
    height = models.FloatField()
    hemoglobin_normal = models.BooleanField(default=False)
    hemoglobin_notes = models.TextField(blank=True, null=True)
    elisa_vh1_positive = models.BooleanField(default=False)
    hepatitisB_positive = models.BooleanField(default=False)
    PPD_positive = models.BooleanField(default=False)
    stool_parasites_positive = models.BooleanField(default=False)
    stool_parasites_notes = models.TextField(blank=True, null=True)
    leukocytes_normal = models.BooleanField(default=False)
    leukocytes_notes = models.TextField(blank=True, null=True)
    nitrites_normal = models.BooleanField(default=False)
    nitrites_notes = models.TextField(blank=True, null=True)
    urobilinogen_normal = models.BooleanField(default=False)
    urobilinogen_notes = models.TextField(blank=True, null=True)
    protein_normal = models.BooleanField(default=False)
    protein_notes = models.TextField(blank=True, null=True)
    pH_normal = models.BooleanField(default=False)
    pH_notes = models.TextField(blank=True, null=True)
    hemoglobin_normal = models.BooleanField(default=False)
    hemoglobin_notes = models.TextField(blank=True, null=True)
    density_normal = models.BooleanField(default=False)
    density_notes = models.TextField(blank=True, null=True)
    glucose_normal = models.BooleanField(default=False)
    glucose_notes = models.TextField(blank=True, null=True)

    class Meta:
        app_label = 'tracker'
        db_table = 'tracker_medicalexampart1'

    def clean(self):
        msg = "This field is required."
        
        if self.bcg_vaccine and self.bcg_vaccine_date is None:
            raise ValidationError(('This field is required'), code='required_error')
        if self.polio_vaccine and self.polio_vaccine_date is None:
            raise ValidationError(('This field is required'), code='required_error')
        if self.dpt_vaccine and self.dpt_vaccine_date is None:
            raise ValidationError(('This field is required'), code='required_error')
        if self.hepatitis_b_vaccine and self.hepatitis_b_vaccine_date is None:
            raise ValidationError(('This field is required'), code='required_error')
        if self.flu_vaccine and self.flu_vaccine_date is None:
            raise ValidationError(('This field is required'), code='required_error')
        if self.yellow_fever_vaccine and self.yellow_fever_vaccine_date is None:
            raise ValidationError(('This field is required'), code='required_error')
        if self.spr_vaccine and self.spr_vaccine_date is None:
            raise ValidationError(('This field is required'), code='required_error')
        if self.hpv_vaccine and self.hpv_vaccine_date is None:
            raise ValidationError(('This field is required'), code='required_error')
        if self.pneumococcal_vaccine and self.pneumococcal_vaccine_date is None:
            raise ValidationError(('This field is required'), code='required_error')
        if self.hemoglobin_normal and self.hemoglobin_notes is None:
            raise ValidationError(('This field is required'), code='required_error')
        if self.stool_parasites_positive and self.stool_parasites_notes is None:
            raise ValidationError(('This field is required'), code='required_error')
        if self.leukocytes_normal and self.leukocytes_notes is None:
            raise ValidationError(('This field is required'), code='required_error')
        if self.nitrites_normal and self.nitrites_notes is None:
            raise ValidationError(('This field is required'), code='required_error')
        if self.urobilinogen_normal and self.urobilinogen_notes is None:
            raise ValidationError(('This field is required'), code='required_error')
        if self.protein_normal and self.protein_notes is None:
            raise ValidationError(('This field is required'), code='required_error')
        if self.pH_normal and self.pH_notes is None:
            raise ValidationError(('This field is required'), code='required_error')
        if self.hemoglobin_normal and self.hemoglobin_notes is None:
            raise ValidationError(('This field is required'), code='required_error')
        if self.density_normal and self.density_notes is None:
            raise ValidationError(('This field is required'), code='required_error')
        if self.glucose_normal and self.glucose_notes is None:
            raise ValidationError(('This field is required'), code='required_error')





            

