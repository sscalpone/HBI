from django.conf.urls import patterns, url

from tracker.views import main
from tracker.views import residence
from tracker.views import child
from tracker.views import operation_history


urlpatterns = patterns('',
    # ex: /tracker/
    url(r'^$', main.index, name='index'),
    url(r'^login/$', main.login, name='login'),
    url(r'^residences/$', residence.index, name='residences'),
    url(r'^residence/(?P<residence_id>\d+)', residence.view, name='residence'),
    url(r'^children/$', child.index, name='children'),
    url(r'^child/new/$', child.new, name='add_child'),
    url(r'^child/(?P<child_id>\d+)', child.view, name='child'),
    url(r'^operation_history/new/(?P<child_id>\d+)', operation_history.new, name='add_operation_history'),
    url(r'^operation_history/(?P<child_id>\d+)', operation_history.view, name='operation_history')
)

