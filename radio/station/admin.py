from django.contrib import admin
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.conf.urls.defaults import *
from .models import Show, Schedule, DJ, Spot 

class ShowAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':['name',]}
    list_display = ('name', 'slug', 'special_program', 'active')
    list_filter = ('name', 'special_program', 'active', 'date_added')
    search_fields = ('name',)
    ordering = ('name',)

class ScheduleAdmin(admin.ModelAdmin):
    list_filter = ('start_date','end_date',)
    list_display = ('start_date', 'end_date', 'get_edit_view', )
    verbose_name = "Schedule"
    verbose_name_plural = "Schedules"

    def get_urls(self):
        urls = super(ScheduleAdmin, self).get_urls()
        my_urls = patterns('',
            url(r'^existing/(?P<schedule_pk>\d+)/', 'radio.station.schedule.views.edit_existing_schedule', name='existing_schedule'),
            url(r'^generate/(?P<schedule_pk>\d+)/', 'radio.station.schedule.views.generate_schedule', name='generate_schedule'),
            url(r'^edit/(?P<schedule_pk>\d+)/', 'radio.station.schedule.views.edit_schedule', name='edit_schedule')
        )
        return my_urls + urls

    def response_add(self, request, obj, *args, **kwargs):
        response = super(ScheduleAdmin, self).response_add(request, obj, *args, **kwargs)
        if isinstance(response, HttpResponseRedirect):
            if response['Location'] in ('../', '../../../'):
                if len(Spot.objects.filter(schedule=obj)[:1]):
                    #we've got a changed schedule object, pass the response back just the same
                    return response
                else:
                    return HttpResponseRedirect(reverse('admin:generate_schedule', kwargs={'schedule_pk':obj.pk}))
        return response

class SpotAdmin(admin.ModelAdmin):
    list_filter = ('schedule', 'repeat_every', 'day_of_week')
    list_display = ('__unicode__', 'dj', 'show', 'schedule', 'offset', 'repeat_every')
    list_editable = ('offset', 'repeat_every')

class DJAdmin(admin.ModelAdmin):
    verbose_name = "DJ Profiles"
    verbose_name = "DJ Profile"
    verbose_name_plural = "DJ Profiles"

admin.site.register(Show, ShowAdmin)
admin.site.register(Schedule, ScheduleAdmin)
admin.site.register(DJ, DJAdmin)
admin.site.register(Spot, SpotAdmin)
