from django.conf.urls.defaults import *

urlpatterns = patterns('radio.station.views',
    url(r'^show/(?P<show_slug>[\w\d\-_]+)/$', 'show_detail', name='show-detail'),
    url(r'^dj/(?P<dj_slug>[\w\d\-_]+)/$', 'dj_detail', name='dj-detail'),
    url(r'^(?P<day_of_week>\d{1})/$', 'for_day', name='for-day'),
    url(r'^schedule/(?P<schedule_pk>\d+)/show/(?P<show_slug>[\w\d\-_]+)/$', 'schedule_show_detail', name='schedule-show-detail'),
    url(r'^schedule/(?P<schedule_pk>\d+)/dj/(?P<dj_slug>[\w\d\-_]+)/$', 'schedule_dj_detail', name='schedule-dj-detail'),
    url(r'^schedule/(?P<schedule_pk>\d+)/(?P<day_of_week>\d{1})/$', 'schedule_for_day', name='schedule-for-day'),
)
