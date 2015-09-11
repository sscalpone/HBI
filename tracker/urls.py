from django.conf.urls import patterns, url

from tracker.views import main
from tracker.views import residence
from tracker.views import child
from tracker.views import dental_exam
from tracker.views import medical_exam_part1
from tracker.views import medical_exam_part2
from tracker.views import psychological_exam
from tracker.views import social_exam
from tracker.views import exam_views

urlpatterns = patterns('',
    # ex: /tracker/
    url(r'^$', main.index, name='index'),
    url(r'^login/$', main.login, name='login'),
    
    url(r'^residences/$', residence.index, name='residences'),
    url(r'^residences/new/$', residence.new, name='add_residence'),
    url(r'^residence/(?P<residence_id>\d+)', residence.view, name='residence'),
    
    url(r'^child/new/(?P<residence_id>\d+)', child.new, name='add_child'),
    url(r'^child/(?P<child_id>\d+)', exam_views.index, name='child'),

    url(r'^dental_exam/(?P<child_id>\d+)/(?P<exam_id>\d+)', dental_exam.view, name='dental_exam'),
    url(r'^dental_exam/new/(?P<child_id>\d+)', dental_exam.new, name='new_dental_exam'),
    url(r'^dental_exam/(?P<child_id>\d+)', dental_exam.index, name='dental_exams'),

    url(r'^medical_exam_part1/(?P<child_id>\d+)/(?P<exam_id>\d+)', medical_exam_part1.view, name='medical_exam_part1'),
    url(r'^medical_exam_part1/new/(?P<child_id>\d+)', medical_exam_part1.new, name='new_medical_exam_part1'),
    url(r'^medical_exam_part1/(?P<child_id>\d+)', medical_exam_part1.index, name='medical_exam_part1s'),

    url(r'^medical_exam_part2/new/(?P<child_id>\d+)/(?P<exam_id>\d+)', medical_exam_part2.view, name='medical_exam_part2'),
    url(r'^medical_exam_part2/new/(?P<child_id>\d+)', medical_exam_part2.new, name='new_medical_exam_part2'),
    url(r'^medical_exam_part2/(?P<child_id>\d+)', medical_exam_part2.index, name='medical_exam_part2s'),

    url(r'^psychological_exam/(?P<child_id>\d+)/(?P<exam_id>\d+)', psychological_exam.view, name='psychological_exam'),
    url(r'^psychological_exam/new/(?P<child_id>\d+)', psychological_exam.new, name='new_psychological_exam'),
    url(r'^psychological_exam/(?P<child_id>\d+)', psychological_exam.index, name='psychological_exams'),

    url(r'^social_exam/(?P<child_id>\d+)/(?P<exam_id>\d+)', social_exam.view, name='social_exam'),
    url(r'^social_exam/new/(?P<child_id>\d+)', social_exam.new, name='new_social_exam'),
    url(r'^social_exam/(?P<child_id>\d+)', social_exam.index, name='social_exams'),
)

