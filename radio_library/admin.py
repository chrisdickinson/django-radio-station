from django.contrib import admin
from models import *

class AlbumInline(admin.TabularInline):
    model = Album

class TrackInline(admin.TabularInline):
    model = Track

class TrackAdmin(admin.ModelAdmin):
    list_display = [ 'name', 'album' ]

class AlbumAdmin(admin.ModelAdmin):
    inlines = [TrackInline]
    list_display = [ 'name', 'artist' ]
    
class ArtistAdmin(admin.ModelAdmin):
    inlines = [AlbumInline]

admin.site.register(Artist,ArtistAdmin)
admin.site.register(Album,AlbumAdmin)
admin.site.register(Track,TrackAdmin)
admin.site.register(Label)
admin.site.register(Genre)
