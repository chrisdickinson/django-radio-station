from django.contrib import admin
from models import *

class LocationAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    pass

class EventAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    pass
admin.site.register(Location, LocationAdmin)
admin.site.register(Event, EventAdmin)
