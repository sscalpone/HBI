from django.conf.urls import patterns, url

from tracker import views

urlpatterns = patterns('',
    # ex: /tracker/
    url(r'^$', views.index, name='index'),
    url(r'^login/$', views.login, name='login'),
    url(r'^main/$', views.main, name='main'),
    url(r'^residence/$', views.residence, name='residence'),
)

