from django.conf.urls.defaults import *


urlpatterns = patterns('radio_station.views',
    url(r'^schedule/((?P<schedule_pk>\d+)/)?(?P<day_of_week>[MTWRFSU]{1}/)?$', 'schedule_weekday', name='schedule-weekday'),
    url(r'^schedule/(?P<schedule_pk>\d+)/(?P<day_of_week>[MTWRFSU0-6]{1})/$', 'schedule_weekday', name='schedule-with-weekday'),
    url(r'^show/((?P<schedule_pk>\d+)/)?(?P<show_slug>[\w\d\-_]+)/$', 'show_detail', name='show-detail'),
    url(r'^dj/((?P<schedule_pk>\d+)/)?(?P<dj_slug>[\w\d\-_]+)/$', 'dj_detail', name='dj-detail'),
)
