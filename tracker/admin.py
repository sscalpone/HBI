from django.contrib import admin

from tracker.models import Child
from tracker.models import Residence
from tracker.models import CustomUser

admin.site.register(Child)
admin.site.register(Residence)
admin.site.register(CustomUser)