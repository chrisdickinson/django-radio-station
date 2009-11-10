from django.contrib import admin
from django.conf.urls.defaults import *
from models import *

class ShowAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':['name',]}
    list_display = ('name', 'slug', 'special_program', 'active')
    list_filter = ('name', 'special_program', 'active', 'date_added')
    search_fields = ('name',)
    ordering = ('name',)

class ScheduleAdmin(admin.ModelAdmin):
    list_filter = ('start_date','end_date',)
    list_display = ('start_date', 'end_date', )
    verbose_name = "Schedule"
    verbose_name_plural = "Schedules"

    def get_urls(self):
        urls = super(ScheduleAdmin, self).get_urls()
        my_urls = patterns('',
            url(r'^existing/(?P<schedule_pk>\d+)/', 'radio_station.schedule.views.edit_existing_schedule', name='existing_schedule'),
            url(r'^generate/(?P<schedule_pk>\d+)/', 'radio_station.schedule.views.generate_schedule', name='generate_schedule'),
            url(r'^edit/(?P<schedule_pk>\d+)/', 'radio_station.schedule.views.edit_schedule', name='edit_schedule')
        )
        return my_urls + urls

class DJAdmin(admin.ModelAdmin):
    verbose_name = "DJ Profiles"
    verbose_name = "DJ Profile"
    verbose_name_plural = "DJ Profiles"

admin.site.register(Show, ShowAdmin)
admin.site.register(Schedule, ScheduleAdmin)
admin.site.register(DJ, DJAdmin)
admin.site.register(Spot)
