from django.conf.urls import patterns, url

from tracker.views import main
from tracker.views import residence
from tracker.views import child
from tracker.views import blood_exam
from tracker.views import consultation_history
from tracker.views import dental_exam
from tracker.views import disease_history
from tracker.views import medical_exam_part1
from tracker.views import medical_exam_part2
from tracker.views import psychological_exam
from tracker.views import operation_history
from tracker.views import social_exam
from tracker.views import exam_views

urlpatterns = patterns('',
    # ex: /tracker/
    url(r'^$', main.index, name='index'),
    url(r'^login/$', main.login, name='login'),
    url(r'^logout/$', main.logout, name='logout'),
    
    url(r'^residences/$', residence.index, name='residences'),
    url(r'^residences/new/$', residence.new, name='add_residence'),
    url(r'^residence/(?P<residence_id>\d+)', residence.view, name='residence'),
    url(r'^residence/edit/(?P<residence_id>\d+)', residence.edit, name='edit_residence'),
    
    url(r'^child/new/(?P<residence_id>\d+)', child.new, name='add_child'),
    url(r'^child/edit/(?P<child_id>\d+)', child.edit, name='edit_child'),
    url(r'^child/(?P<child_id>\d+)', exam_views.index, name='child'),

    url(r'^blood_exam/(?P<child_id>\d+)/(?P<exam_id>\d+)', blood_exam.view, name='blood_exam'),
    url(r'^blood_exam/edit/(?P<child_id>\d+)/(?P<exam_id>\d+)', blood_exam.edit, name='edit_blood_exam'),
    url(r'^blood_exam/new/(?P<child_id>\d+)', blood_exam.new, name='new_blood_exam'),

    url(r'^dental_exam/(?P<child_id>\d+)/(?P<exam_id>\d+)', dental_exam.view, name='dental_exam'),
    url(r'^dental_exam/edit/(?P<child_id>\d+)/(?P<exam_id>\d+)', dental_exam.edit, name='edit_dental_exam'),
    url(r'^dental_exam/new/(?P<child_id>\d+)', dental_exam.new, name='new_dental_exam'),

    url(r'^consultation_history/(?P<child_id>\d+)/(?P<exam_id>\d+)', consultation_history.view, name='consultation_history'),
    url(r'^consultation_history/edit/(?P<child_id>\d+)/(?P<exam_id>\d+)', consultation_history.edit, name='edit_consultation_history'),
    url(r'^consultation_history/new/(?P<child_id>\d+)', consultation_history.new, name='new_consultation_history'),

    url(r'^disease_history/(?P<child_id>\d+)/(?P<exam_id>\d+)', disease_history.view, name='disease_history'),
    url(r'^disease_history/edit/(?P<child_id>\d+)/(?P<exam_id>\d+)', disease_history.edit, name='edit_disease_history'),
    url(r'^disease_history/new/(?P<child_id>\d+)', disease_history.new, name='new_disease_history'),

    url(r'^medical_exam_part1/(?P<child_id>\d+)/(?P<exam_id>\d+)', medical_exam_part1.view, name='medical_exam_part1'),
    url(r'^medical_exam_part1/edit/(?P<child_id>\d+)/(?P<exam_id>\d+)', medical_exam_part1.edit, name='edit_medical_exam_part1'),
    url(r'^medical_exam_part1/new/(?P<child_id>\d+)', medical_exam_part1.new, name='new_medical_exam_part1'),

    url(r'^medical_exam_part2/new/(?P<child_id>\d+)/(?P<exam_id>\d+)', medical_exam_part2.view, name='medical_exam_part2'),
    url(r'^medical_exam_part2/edit/(?P<child_id>\d+)/(?P<exam_id>\d+)', medical_exam_part2.edit, name='edit_medical_exam_part2'),
    url(r'^medical_exam_part2/new/(?P<child_id>\d+)', medical_exam_part2.new, name='new_medical_exam_part2'),

    url(r'^operation_history/(?P<child_id>\d+)/(?P<exam_id>\d+)', operation_history.view, name='operation_history'),
    url(r'^operation_history/edit/(?P<child_id>\d+)/(?P<exam_id>\d+)', operation_history.edit, name='edit_operation_history'),
    url(r'^operation_history/new/(?P<child_id>\d+)', operation_history.new, name='new_operation_history'),

    url(r'^psychological_exam/(?P<child_id>\d+)/(?P<exam_id>\d+)', psychological_exam.view, name='psychological_exam'),
    url(r'^psychological_exam/edit/(?P<child_id>\d+)/(?P<exam_id>\d+)', psychological_exam.edit, name='edit_psychological_exam'),
    url(r'^psychological_exam/new/(?P<child_id>\d+)', psychological_exam.new, name='new_psychological_exam'),

    url(r'^social_exam/(?P<child_id>\d+)/(?P<exam_id>\d+)', social_exam.view, name='social_exam'),
    url(r'^social_exam/edit/(?P<child_id>\d+)/(?P<exam_id>\d+)', social_exam.edit, name='edit_social_exam'),
    url(r'^social_exam/new/(?P<child_id>\d+)', social_exam.new, name='new_social_exam'),
)

