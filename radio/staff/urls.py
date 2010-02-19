from django.conf.urls.defaults import *

urlpatterns = patterns('radio.staff.views',
    url(r'^(?P<schedule_pk>\d+)/$', 'staff_list_for_schedule', name='staff-list-for-schedule'),
    url(r'^$', 'staff_list', name='staff-list'),
)
