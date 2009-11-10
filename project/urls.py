
from django.conf.urls.defaults import patterns, include, handler500
from django.conf import settings
from django.contrib import admin
import d51_django_admin_piston

handler500 # Pyflakes

admin.autodiscover()
d51_django_admin_piston.autodiscover(admin.site)

urlpatterns = patterns(
    '',
    (r'^logs/', include('radio_logs.urls')),
    (r'^events/', include('radio_events.urls')),
    (r'^station/', include('radio_station.urls')),
    (r'^admin/', include(admin.site.urls)),
    (r'^accounts/login/$', 'django.contrib.auth.views.login'),
    (r'^', include('frontend.urls')),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve',
         {'document_root': settings.MEDIA_ROOT}),
    )
