from django.db import models

from django.contrib.auth.models import User

class Residence(models.Model):
    residence_name = models.CharField(max_length=200)

    def __unicode__(self):
        return self.residence_name

class Admin(models.Model):
    user = models.OneToOneField(User)

    def __unicode__(self):
        return self.user.username

class Medical(models.Model):
    user = models.OneToOneField(User)

    def __unicode__(self):
        return self.user.username

class MedicalAdmin(models.Model):
    user = models.OneToOneField(User)

    def __unicode__(self):
        return self.user.username

class ResidenceDirector(models.Model):
    user = models.OneToOneField(User)
    residence = models.ForeignKey(Residence)

    def __unicode__(self):
        return self.user.username

class ResidenceParent(models.Model):
    user = models.OneToOneField(User)
    residence = models.ForeignKey(Residence)

    def __unicode__(self):
        return self.user.username

class Child(models.Model):
    residence = models.ForeignKey(Residence)
    first_name1 = models.CharField(max_length=200)
    first_name2 = models.CharField(max_length=200)
    last_name1 = models.CharField(max_length=200)
    last_name2 = models.CharField(max_length=200)
    birthdate = models.DateField()
    birthplace = models.CharField(max_length=200)
    intake_date = models.DateField()
    photo = models.ImageField(upload_to='photos')

    def __unicode__(self):
        return self.first_name1

class BasicInfo(models.Model):
    child = models.ForeignKey(Child)

class SocialExamInfo(models.Model):
    child = models.ForeignKey(Child)
    date = models.DateField()
    has_birth_certificate = models.BooleanField()
    original_birth_certificate = models.BooleanField()
    dni = models.BooleanField()
    dni_in_process = models.BooleanField()
    dni_comments = models.TextField()
    sis = models.BooleanField()
    sis_in_process = models.BooleanField()
    sis_comments = models.TextField()
    antecedents = models.TextField()
    family_situation = models.TextField()
    health_situation = models.TextField()
    housing_situation = models.TextField()
    enconomic_situation = models.TextField()
    general_comments = models.TextField()
    visitors_allowed = models.BooleanField()
    visitors_notes = models.TextField()
    social_diagnosis = models.TextField()
    recommendation = models.TextField()

class SocialExamInfo(models.Model):
    child = models.ForeignKey(Child)
    date = models.DateField()
    family_notes = models.TextField()
    physical_description = models.TextField()
    intelectual_notes = models.TextField()
    organicity_notes = models.TextField()
    psychomotor_notes = models.TextField()
    emotional_notes = models.TextField()
    recommendation = models.TextField()

class SocialExamDiagnosis(models.Model):
    title = models.CharField(max_length=200)
    dwmq = models.CharField(max_length=200)
    exam = models.ForeignKey(SocialExamInfo)

class MedicalExamPart1Info(models.Model):
    child = models.ForeignKey(Child)
    date = models.DateField()
    bcg_vaccine = models.BooleanField()
    bcg_vaccine_date = models.DateField()
    polio_vaccine = models.BooleanField()
    polio_vaccine_date = models.DateField()
    dpt_vaccine = models.BooleanField()
    dpt_vaccine_date = models.DateField()
    hepatitis_b_vaccine = models.BooleanField()
    hepatitis_b_vaccine_date = models.DateField()
    flu_vaccine = models.BooleanField()
    flu_vaccine_date = models.DateField()
    yellow_fever_vaccine = models.BooleanField()
    yellow_fever_vaccine_date = models.DateField()
    spr_vaccine = models.BooleanField()
    spr_vaccine_date = models.DateField()
    hpv_vaccine = models.BooleanField()
    hpv_vaccine_date = models.DateField()
    pneumococcal_vaccine = models.BooleanField()
    pneumococcal_vaccine_date = models.DateField()
    weight = models.FloatField()
    height = models.FloatField()

class MedicalExamPart2Info(models.Model):
    child = models.ForeignKey(Child)
    date = models.DateField()
    illness_notes = models.TextField()
    appetite_notes = models.TextField()
    sleep_notes = models.TextField()
    visual_acuity_right = models.CharField(max_length=200)
    visual_acuity_left = models.CharField(max_length=200)
    appearance_notes = models.TextField()
    skin_notes = models.TextField()
    lymph_notes = models.TextField()
    neck_notes = models.TextField()
    lung_notes = models.TextField()
    cardio_notes = models.TextField()
    abdomen_notes = models.TextField()
    genitourinary_notes = models.TextField()
    extremities_notes = models.TextField()
    neurological_notes = models.TextField()
    treatment_notes = models.TextField()
    recommendation = models.TextField()

class MedicalExamDiagnosis(models.Model):
    exam = models.ForeignKey(MedicalExamPart2Info)
    name = models.CharField(max_length=200)
    value = models.TextField()

class DentalExam(models.Model):
    child = models.ForeignKey(Child)
    date = models.DateField()
    recommendation = models.TextField()

class DentalExamDiagnosis(models.Model):
    exam = models.ForeignKey(DentalExam)
    notes = models.TextField()

class BloodExam(models.Model):
    child = models.ForeignKey(Child)
    date = models.DateField()
    hemogloban_normal = models.BooleanField()
    hemogloban_notes = models.TextField()
    elisa_vh1_normal = models.BooleanField()
    elisa_vh1_notes = models.TextField()
    hepatitis_b_normal = models.BooleanField()
    hepatitis_b_notes = models.TextField()
    ppd_normal = models.BooleanField()
    ppd_notes = models.TextField()
    orina_normal = models.BooleanField()
    orina_notes = models.TextField()
    white_cells_normal = models.BooleanField()
    white_cells_notes = models.TextField()
    nitrites_normal = models.BooleanField()
    nitrites_notes = models.TextField()
    urobilinogen_normal = models.BooleanField()
    urobilinogen_notes = models.TextField()
    protein_normal = models.BooleanField()
    protein_notes = models.TextField()
    ph_normal = models.BooleanField()
    ph_notes = models.TextField()
    density_normal = models.BooleanField()
    density_notes = models.TextField()
    glucoce_normal = models.BooleanField()
    glucoce_notes = models.TextField()

class BloodParasite(models.Model):
    exam = models.ForeignKey(BloodExam)
    parasite = models.CharField(max_length=200)

