from django.conf.urls.defaults import *

urlpatterns = patterns('radio_station.views',
    url(r'^schedule/list', 'schedule_list', name='schedule-list'), 
    url(r'^schedule/(?P<schedule_pk>\d+)/metrics', 'schedule_metrics', name='schedule-metrics'), 
    url(r'^schedule/(?P<schedule_pk>\d+)', 'schedule_spot_list', name='schedule-spots'), 
    url(r'^schedule/', 'schedule_spot_list', name='schedule-spots-current'),
    url(r'spot/(?P<spot_pk>\d+)', 'spot_detail', name='spot-detail'),
    url(r'dj/(?P<dj_slug>[\w\d\-_]+)', 'dj_detail', name='dj-detail'),
    url(r'show/(?P<show_slug>[\w\d\-_]+)', 'show_detail', name='show-detail'),
)
