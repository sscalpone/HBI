from django.conf.urls import patterns, url

from tracker.views import main
from tracker.views import residence
from tracker.views import child
from tracker.views import disease_history
from tracker.views import operation_history
from tracker.views import consultation_history
from tracker.views import dental_exam
from tracker.views import psychological_exam_info


urlpatterns = patterns('',
    # ex: /tracker/
    url(r'^$', main.index, name='index'),
    url(r'^login/$', main.login, name='login'),
    url(r'^residences/$', residence.index, name='residences'),
    url(r'^residence/(?P<residence_id>\d+)', residence.view, name='residence'),
    url(r'^children/$', child.index, name='children'),
    url(r'^child/new/$', child.new, name='add_child'),
    url(r'^child/(?P<child_id>\d+)', child.view, name='child'),
    url(r'^disease_history/new/(?P<child_id>\d+)', disease_history.new, name='add_disease_history'),
    url(r'^disease_history/(?P<child_id>\d+)', disease_history.view, name='disease_history'),
    url(r'^operation_history/new/(?P<child_id>\d+)', operation_history.new, name='add_operation_history'),
    url(r'^operation_history/(?P<child_id>\d+)', operation_history.view, name='operation_history'),
    url(r'^consultation_history/new/(?P<child_id>\d+)', consultation_history.new, name='add_consultation_history'),
    url(r'^consultation_history/(?P<child_id>\d+)', consultation_history.view, name='consultation_history'),
    url(r'^dental_exam/new/(?P<child_id>\d+)', dental_exam.new, name='add_dental_exam'),
    url(r'^dental_exam/(?P<child_id>\d+)', dental_exam.view, name='dental_exam'),
    url(r'^psychological_exam_info/new/(?P<child_id>\d+)', psychological_exam_info.new, name='add_psychological_exam_info'),
    url(r'^psychological_exam_info/(?P<child_id>\d+)', psychological_exam_info.view, name='psychological_exam_info'),
)

