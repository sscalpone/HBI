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
    birthdate = models.DateField();
    birthplace = models.CharField(max_length=200);
    intake_date = models.DateField();
    photo = models.ImageField('photos')

    def __unicode__(self):
        return self.name

class BasicInfo(models.Model):
    child = models.ForeignKey(Child)

class ExamInfo(models.Model):
    child = models.ForeignKey(Child)

