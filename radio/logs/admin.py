from django.contrib import admin
from django.conf import settings
from django.conf.urls.defaults import *
from django.db.models import Count, Sum
from radio.station.models import Spot
from .models import *

class RequestAdmin(admin.ModelAdmin):
    list_display = ('what', 'who', 'when', 'ip')
    search_fields = ('what', 'who')
    list_filter = ('ip', 'when')
    verbose_name = "Request"
    verbose_name_plural = "Requests"

class EntryAdmin(admin.ModelAdmin):
    list_display = ('artist', 'track', 'album', 'genre', 'submitted', 'dj')
    list_filter = ('genre', 'submitted', 'is_rotation',)
    fields = ('artist', 'track', 'album', 'genre', 'is_rotation')
    verbose_name = "Entry"
    verbose_name_plural = "Entries"
    radio.fields = {'genre':admin.VERTICAL}

    def save_model(self, request, obj, form, change):
        if hasattr(obj, 'dj'):
            obj.dj = request.user.get_profile()
        try:
            if obj.show in (None, ''):
                obj.show = Spot.objects.get_current_spot().show
        except:
            pass
        return super(self.__class__, self).save_model(request, obj, form, change)

    class Media:
        js = ('site/js/ac_global_fns.js', 'site/js/last_logs.js')
        
admin.site.register(Request, RequestAdmin)
admin.site.register(Entry, EntryAdmin)
