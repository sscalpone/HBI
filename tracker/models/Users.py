import datetime

from Residence import Residence

from django.db import models

from django.contrib.auth.models import User

class Admin(models.Model):
    user = models.OneToOneField(User)

    def __unicode__(self):
        return self.user.username

    class Meta:
        app_label = 'tracker'
        db_table = 'tracker_admin'

class Medical(models.Model):
    user = models.OneToOneField(User)

    def __unicode__(self):
        return self.user.username

    class Meta:
        app_label = 'tracker'
        db_table = 'tracker_medical'

class MedicalAdmin(models.Model):
    user = models.OneToOneField(User)

    def __unicode__(self):
        return self.user.username

    class Meta:
        app_label = 'tracker'
        db_table = 'tracker_medicaladmin'

class ResidenceDirector(models.Model):
    user = models.OneToOneField(User)
    residence = models.ForeignKey(Residence)

    def __unicode__(self):
        return self.user.username

    class Meta:
        app_label = 'tracker'
        db_table = 'tracker_residencedirector'

class ResidenceParent(models.Model):
    user = models.OneToOneField(User)
    residence = models.ForeignKey(Residence)

    def __unicode__(self):
        return self.user.username

    class Meta:
        app_label = 'tracker'
        db_table = 'tracker_residenceparent'

