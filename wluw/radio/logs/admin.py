from django.contrib import admin
from django.conf import settings
from django.conf.urls.defaults import *
from django.db.models import Count, Sum
from radio.station.models import Spot
from .models import Entry 
import datetime
from wluw.radio.library.tasks import grab_album_art, ping_nodejs_with

class EntryAdmin(admin.ModelAdmin):
    list_display = ('artist', 'track', 'album', 'genre', 'submitted', 'dj')
    list_filter = ('genre', 'submitted', 'is_rotation',)
    fields = ('artist', 'track', 'album', 'genre', 'is_rotation')
    verbose_name = "Entry"
    verbose_name_plural = "Entries"
    radio_fields = {'genre':admin.VERTICAL}

    def save_model(self, request, obj, form, change):
        if not hasattr(obj, 'dj'):
            obj.dj = request.user.dj
        try:
            now = datetime.datetime.now()
            if obj.show in (None, ''):
                obj.show = Spot.objects.get_current_spot(now).show
        except:
            pass

        result = super(EntryAdmin, self).save_model(request, obj, form, change)

        if obj.album.status == 0:
            grab_album_art.delay(obj.album.pk, obj.pk)
        else:
            ping_nodejs_with.delay(obj.pk)

        return result

    class Media:
        js = ('site/js/ac_global_fns.js', 'site/js/last_logs.js')
        
admin.site.register(Entry, EntryAdmin)
