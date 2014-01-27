from django.conf.urls import patterns, url

from tracker import views

urlpatterns = patterns('',
    # ex: /tracker/
    url(r'^$', views.index, name='index'),
    url(r'^login/$', views.login, name='login'),
    url(r'^main/$', views.main, name='main'),
    url(r'^residence/$', views.residence, name='residence'),
    url(r'^children/$', views.children, name='children'),
    url(r'^children/new/$', views.add_child, name='add_child'),
    url(r'^children/view/(?P<child_id>\d+)', views.child, name='child')
)

