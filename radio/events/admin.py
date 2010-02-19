from django.contrib import admin
from models import *

class LocationAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    pass

class EventAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    list_display = ['name', 'location', 'date', 'time_start', 'time_end', 'get_absolute_url']
    date_hierarchy = 'date'
    save_as = True
    search_fields = ['name', 'location__name']
    pass
admin.site.register(Location, LocationAdmin)
admin.site.register(Event, EventAdmin)
