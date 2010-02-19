from django.conf.urls.defaults import *


urlpatterns = patterns('radio.logs.views',
    url(r'^$', 'time_view', name='logs-time-now'),
    url(r'^charts/(?P<year>\d{4})/(?P<month>\d{1,2})/(?P<week>\d{1})(/(?P<what>artist|album))?(/(?P<rotation>rotation))?/$', 'chart_view', name='charts-view'),
    url(r'^(?P<year>\d{4})/(?P<month>\w{3})/(?P<day>\d{1,2})/(?P<hour>\d{1,2})/$', 'time_view', name='logs-time'),
)
