from django.conf import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.views.generic import RedirectView
from django.contrib import admin
from django.contrib.sites.models import Site

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()
# admin.site.unregister(Site)

urlpatterns = patterns('',
    url(r'^$', RedirectView.as_view(url='/tracker/')),
    url(r'^tracker/', include('tracker.urls', namespace="tracker")),
    url(r'^admin/', include(admin.site.urls)),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^assets/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.ASSETS_ROOT})
    ) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
