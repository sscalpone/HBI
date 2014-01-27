import datetime

from Residence import Residence

from django.db import models

from django.contrib.auth.models import User

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

    class Meta:
        app_label = 'tracker'
        db_table = 'tracker_child'

    def __unicode__(self):
        return self.first_name1

    def age(self):
        return self.age_in_years(self.birthdate, datetime.datetime.utcnow())

    def age_in_years(self, from_date, to_date, leap_day_anniversary_Feb28=True):
        computed_age = to_date.year - from_date.year
        try:
            anniversary = from_date.replace(year=to_date.year)
        except ValueError:
            assert from_date.day == 29 and from_date.month == 2
            if leap_day_anniversary_Feb28:
                anniversary = datetime.date(to_date.year, 2, 28)
            else:
                anniversary = datetime.date(to_date.year, 3, 1)
            if to_date < anniversary:
                computed_age -= 1
        return computed_age

