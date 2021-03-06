# coding=utf-8

import datetime
import uuid

from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import UserManager
from django.contrib.auth.models import PermissionsMixin

from Residence import Residence


"""This model creates custom fields for the User model, since the default
User model is basic and difficult to build upon when using UUIDs. It uses
the built-in Django authentication, it just has more fields.
"""


class CustomUser(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=30, unique=True)
    uuid = models.CharField(max_length=200, unique=True, default=uuid.uuid4)
    first_name = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=50, blank=True)
    email = models.EmailField(max_length=200, blank=True)
    is_staff = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    last_saved = models.DateTimeField(default=datetime.datetime.utcnow)
    date_joined = models.DateTimeField(default=datetime.datetime.utcnow)
    residence = models.ForeignKey(Residence, blank=True, null=True,
                                  default=None)
    add_users = models.BooleanField(default=False)
    delete_info = models.BooleanField(default=False)
    add_edit_forms = models.BooleanField(default=False)
    not_restricted_to_home = models.BooleanField(default=False)
    view = models.BooleanField(default=True)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    # Returns the first name of the user
    def get_short_name(self):
        return self.first_name

    # Returns the first and last name of the user
    def get_full_name(self):
        return self.first_name + ' ' + self.last_name

    # Returns the user's username
    def __unicode__(self):
        return self.username

    # Meta class defines database table and labels, and clears any
    # default permissions. It also adds custom permissions.
    class Meta:
        app_label = 'tracker'
        db_table = 'tracker_customuser'
        default_permissions = ()

        # Permissions used by users in this app
        permissions = (
            ('add_users', 'Add Users'),
            ('delete_info', 'Delete Info'),
            ('add_edit_forms', 'Add and Edit Forms'),
            ('view', 'View'),
            ('not_restricted_to_home', 'Not Restricted to Home'),
        )
