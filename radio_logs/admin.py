from django.contrib import admin
from django.conf.urls.defaults import *
from django.http import HttpResponseRedirect
from django.db.models import Count, Sum
from radio_library.models import *
from models import *

class RequestAdmin(admin.ModelAdmin):
    list_display = ('what', 'who', 'when', 'ip')
    search_fields = ('what', 'who')
    list_filter = ('ip', 'when')
    verbose_name = "Request"
    verbose_name_plural = "Requests"

class EntryAdmin(admin.ModelAdmin):
    list_display = ('artist', 'track', 'album', 'genre', 'submitted', 'dj', 'playcount')
    list_filter = ('genre', 'submitted',)
    verbose_name = "Entry"
    verbose_name_plural = "Entries"

    def playcount(self, obj):
        return obj.playcount 

    def build_extra_context_for_request(self, request):
        user = request.user
        entries = Entry.objects.filter(dj__account=request.user).order_by('submitted')[:30]
        return {
            'entries':entries
        }

    def add_view(self, request, extra_context=None):
        extra_context = self.build_extra_context_for_request(request)
        return super(EntryAdmin, self).add_view(request, extra_context) 

    def change_view(self, request, object_id, extra_context=None):
        extra_context = self.build_extra_context_for_request(request)
        return super(EntryAdmin, self).change_view(request, object_id, extra_context) 

    class Media:
        js = ('site/js/ac_global_fns.js', 'site/js/last_logs.js')
        
admin.site.register(Request, RequestAdmin)
admin.site.register(Entry, EntryAdmin)
