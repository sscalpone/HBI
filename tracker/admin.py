from django.contrib import admin
from tracker.models import Child
from tracker.models import Residence
from tracker.models import ResidenceDirector
from tracker.models import ResidenceParent

class ResidenceDirectorInline(admin.TabularInline):
	model = ResidenceDirector
	extra = 1

class ResidenceParentInline(admin.TabularInline):
	model = ResidenceParent
	extra = 1

class ChildInline(admin.TabularInline):
	model = Child
	extra = 3

class ResidenceAdmin(admin.ModelAdmin):
	inlines = [ResidenceDirectorInline, ResidenceParentInline, ChildInline]

admin.site.register(Residence, ResidenceAdmin)

admin.site.register(ResidenceDirector)

