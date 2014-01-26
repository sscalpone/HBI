from django.contrib import admin
from polls.models import Choice
from polls.models import Question

class ChoiceInline(admin.TabularInline):
	model = Choice
	extra = 3

class QuestionAdmin(admin.ModelAdmin):
#	fields = [ 'pub_date', 'question_text' ]
	fieldsets = [
		(None, { 'fields' : ['question_text']}),
		('Date information', { 'fields' : ['pub_date'], 'classes': ['collapse']}),
	]
	inlines = [ChoiceInline]
	list_filter = ['pub_date']
	list_display = ('question_text', 'pub_date', 'was_published_recently')


admin.site.register(Question, QuestionAdmin)

admin.site.register(Choice)

