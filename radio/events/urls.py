from django.conf.urls.defaults import *

urlpatterns = patterns('radio.events.views',
    url('^(?P<slug>[a-zA-Z0-9\-]+)/$', 'events_for_location', name='events-for-location'),
    url('^(?P<year>\d+)/(?P<month>\d{1,2})/(?P<day>\d{1,2})/(?P<slug>[a-zA-Z0-9\-_]+)', 'event_detail', name='event-detail'),
    url('^(?P<year>\d+)/(?P<month>\d{1,2})/(?P<day>\d{1,2})', 'events_for_day', name='events-for-day'),
    url('^$', 'events_for_day', name='events-list'), 
)
