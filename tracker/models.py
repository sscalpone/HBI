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
    photo = models.ImageField('photos')

    def __unicode__(self):
        return self.name

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

