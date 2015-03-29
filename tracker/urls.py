from django.conf.urls import patterns, url

from tracker.views import main
from tracker.views import residence
from tracker.views import child
from tracker.views import dental_exam
from tracker.views import medical_exam_part1
from tracker.views import medical_exam_part2
from tracker.views import psychological_exam
from tracker.views import social_exam

urlpatterns = patterns('',
    # ex: /tracker/
    url(r'^$', main.index, name='index'),
    url(r'^login/$', main.login, name='login'),
    url(r'^residences/$', residence.index, name='residences'),
    url(r'^residence/(?P<residence_id>\d+)', residence.view, name='residence'),
    url(r'^children/$', child.index, name='children'),
    url(r'^child/new/$', child.new, name='add_child'),
    url(r'^child/(?P<child_id>\d+)', child.view, name='child'),

    url(r'^dental_exam/new/(?P<child_id>\d+)', dental_exam.new, name='new_dental_exam'),
    url(r'^dental_exam/(?P<child_id>\d+)', dental_exam.view, name='dental_exam'),

    url(r'^medical_exam_part1/new/(?P<child_id>\d+)', medical_exam_part1.new, name='new_medical_exam_part1'),
    url(r'^medical_exam_part1/(?P<child_id>\d+)', medical_exam_part1.view, name='medical_exam_part1'),

    url(r'^medical_exam_part2/new/(?P<child_id>\d+)', medical_exam_part2.new, name='new_medical_exam_part2'),
    url(r'^medical_exam_part2/(?P<child_id>\d+)', medical_exam_part2.view, name='medical_exam_part2'),

    url(r'^psychological_exam/new/(?P<child_id>\d+)', psychological_exam.new, name='new_psychological_exam'),
    url(r'^psychological_exam/(?P<child_id>\d+)', psychological_exam.view, name='psychological_exam'),

    url(r'^social_exams/new/(?P<child_id>\d+)', social_exam.new, name='new_social_exam'),
    url(r'^social_exams/(?P<child_id>\d+)', social_exam.index, name='social_exams'),
    url(r'^social_exam/(?P<exam_id>\d+)', social_exam.view, name='social_exam'),

)

