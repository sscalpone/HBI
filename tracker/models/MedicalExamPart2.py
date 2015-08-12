import datetime

from Child import Child
from Signature import Signature

from django.db import models

from django.contrib.auth.models import User

class MedicalExamPart2(models.Model):
    child = models.ForeignKey(Child)
    date = models.DateField()
    illness_notes = models.TextField()
    appetite_notes = models.TextField()
    sleep_notes = models.TextField()
    concerns_notes = models.TextField()
    blood_pressure = models.TextField()
    pulse = models.TextField()
    visual_acuity_left = models.TextField()
    visual_acuity_right = models.TextField()
    appearance_normal = models.BooleanField(default=False)
    appearance_notes = models.TextField(blank=True, null=True)
    skin_mucosa_normal = models.BooleanField(default=False)
    skin_mucosa_notes = models.TextField(blank=True, null=True)
    TCSC_lymph_normal = models.BooleanField(default=False)
    TCSC_lymph_notes = models.TextField(blank=True, null=True)
    head_neck_normal = models.BooleanField(default=False)
    head_neck_notes = models.TextField(blank=True, null=True)
    thorax_lungs_normal = models.BooleanField(default=False)
    thorax_lungs_notes = models.TextField(blank=True, null=True)
    cardio_normal = models.BooleanField(default=False)
    cardio_notes = models.TextField(blank=True, null=True)
    abdomen_normal = models.BooleanField(default=False)
    abdomen_notes = models.TextField(blank=True, null=True)
    genitourinary_normal = models.BooleanField(default=False)
    genitourinary_notes = models.TextField(blank=True, null=True)
    extremities_normal = models.BooleanField(default=False)
    extremities_notes = models.TextField(blank=True, null=True)
    neurological_normal = models.BooleanField(default=False)
    neurological_notes = models.TextField(blank=True, null=True)
    recommendations = models.TextField()

    class Meta:
        app_label = 'tracker'
        db_table = 'tracker_medicalexampart2'

    def clean(self):
        msg = "This field is required."
        
        if self.appearance_normal and self.appearance_notes is None:
            raise ValidationError(('This field is required'), code='required_error')
        if self.skin_mucosa_normal and self.skin_mucosa_notes is None:
            raise ValidationError(('This field is required'), code='required_error')
        if self.TCSC_lymph_normal and self.TCSC_lymph_notes is None:
            raise ValidationError(('This field is required'), code='required_error')
        if self.head_neck_normal and self.head_neck_notes is None:
            raise ValidationError(('This field is required'), code='required_error')
        if self.thorax_lungs_normal and self.thorax_lungs_notes is None:
            raise ValidationError(('This field is required'), code='required_error')
        if self.cardio_normal and self.cardio_notes is None:
            raise ValidationError(('This field is required'), code='required_error')
        if self.abdomen_normal and self.abdomen_notes is None:
            raise ValidationError(('This field is required'), code='required_error')
        if self.genitourinary_normal and self.genitourinary_notes is None:
            raise ValidationError(('This field is required'), code='required_error')
        if self.extremities_normal and self.extremities_notes is None:
            raise ValidationError(('This field is required'), code='required_error')
        if self.neurological_normal and self.neurological_notes is None:
            raise ValidationError(('This field is required'), code='required_error')

class CurrentMedsList(models.Model):
    exam = models.ForeignKey(MedicalExamPart2)
    med_name = models.TextField()
    dose = models.TextField()
    frequency = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()

    class Meta:
        app_label = 'tracker'
        db_table = 'tracker_currentmedslist'

class PastMedsList(models.Model):
    exam = models.ForeignKey(MedicalExamPart2)
    med_name = models.TextField()
    dose = models.TextField()
    frequency = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()

    class Meta:
        app_label = 'tracker'
        db_table = 'tracker_pastmedslist'

class MedicalExamDiagnosis(models.Model):
    exam = models.ForeignKey(MedicalExamPart2)
    name = models.TextField()
    value = models.TextField()

    class Meta:
        app_label = 'tracker'
        db_table = 'tracker_medicalexamdiagnosis'

