
from django.conf.urls.defaults import patterns, include, handler500, handler404
from django.conf import settings
from django.contrib import admin
import d51_django_admin_piston

handler500 = 'radio.frontend.views.server_error'

admin.autodiscover()
d51_django_admin_piston.autodiscover(admin.site)

urlpatterns = patterns(
    '',
    (r'^logs/', include('radio.logs.urls')),
    (r'^events/', include('radio.events.urls')),
    (r'^station/', include('radio.station.urls')),
    (r'^staff/', include('radio.staff.urls')),
    (r'^admin/', include(admin.site.urls)),
    (r'^accounts/login/$', 'django.contrib.auth.views.login'),
    (r'^', include('radio.frontend.urls')),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve',
         {'document_root': settings.MEDIA_ROOT}),
    )
