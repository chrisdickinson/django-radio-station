from django.contrib import admin
from django.conf.urls.defaults import *
from django.http import HttpResponseRedirect
from django.db.models import Count, Sum
from radio_library.models import *
from radio_station.models import Spot
from radio_twitter.models import PendingUpdate
from models import *
from django.conf import settings

TWEET_ENTRIES = getattr(settings, 'RADIO_LOGS_TWEET_LOGS', False)

class RequestAdmin(admin.ModelAdmin):
    list_display = ('what', 'who', 'when', 'ip')
    search_fields = ('what', 'who')
    list_filter = ('ip', 'when')
    verbose_name = "Request"
    verbose_name_plural = "Requests"

class EntryAdmin(admin.ModelAdmin):
    list_display = ('artist', 'track', 'album', 'genre', 'submitted', 'dj')
    list_filter = ('genre', 'submitted', 'is_rotation',)
    exclude = ('dj', 'show',)
    verbose_name = "Entry"
    verbose_name_plural = "Entries"
    radio_fields = {'genre':admin.VERTICAL}

    def post_pending_update(self, entry):
        fields = [
            entry.artist.name,
            entry.album.name,
            entry.track.name,
        ]
        length = sum([len(x) for x in fields])
        if length > 134 or entry.album.name == '<Untitled Album>':
            fields = [ entry.artist.name, entry.track.name ]
        length = sum([len(x) for x in fields])
        if length > 134:
            fields = [ entry.artist.name[:60], entry.track.name[:60] ]
        status = ' - '.join(fields)
        update = PendingUpdate(status=status, has_posted=False)
        update.save()

    def save_model(self, request, obj, form, change):
        try:
            getattr(obj, 'dj')
        except:
            obj.dj = request.user.get_profile()
        try:
            if obj.show in (None, ''):
                obj.show = Spot.objects.get_current_spot().show
        except:
            pass
        if TWEET_ENTRIES:
            self.post_pending_update(obj)
        return super(self.__class__, self).save_model(request, obj, form, change)

    class Media:
        js = ('site/js/ac_global_fns.js', 'site/js/last_logs.js')
        
admin.site.register(Request, RequestAdmin)
admin.site.register(Entry, EntryAdmin)
