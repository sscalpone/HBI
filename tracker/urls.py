from django.conf.urls import patterns, url

from tracker.views import main
from tracker.views import residence
from tracker.views import child


urlpatterns = patterns('',
    # ex: /tracker/
    url(r'^$', main.index, name='index'),
    url(r'^login/$', main.login, name='login'),
    url(r'^residences/$', residence.index, name='residences'),
    url(r'^residence/(?P<residence_id>\d+)', residence.view, name='residence'),
    url(r'^children/$', child.index, name='children'),
    url(r'^child/new/$', child.new, name='add_child'),
    url(r'^child/(?P<child_id>\d+)', child.view, name='child')
)

