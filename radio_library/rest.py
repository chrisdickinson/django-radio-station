import simplerest
from simplerest.interface import RestInterface
from django.db.models import Count
from models import *
class ArtistInterface(RestInterface):
    name = 'artists'
    model = Artist
    queryable_fields = ['pk', 'name', 'album']
    return_fields = ['pk', 'name', 'albums']
    allowed_queries = ['exact', 'gt', 'lt', 'contains', 'startswith']
    paginate = 15

    def get_albums(self, obj, attr):
        album_names = []
        albums = obj.album_set.get_query_set()
        for album in albums:
            album_names.append(album.name)
        return album_names

class ChartInterface(RestInterface):
    name = 'charts'
    model = Artist
    queryable_fields = ['pk', 'name', 'album', 'playcount', 'entry']
    return_fields = ['pk', 'name', 'playcount', 'album_set', 'entry_set']
    allowed_queries = ['exact', 'gt', 'lt', 'gte', 'lte', 'range', 'in', 'contains', 'startswith']
    paginate = 15
    def get_queryset(self):
        return self.model.objects.all().annotate(playcount=Count('entry')) 

    def get_album_set(self, obj, attr):
        print attr
        return {}

    def get_entry_set(self, obj, attr):
        print attr
        return {}

class AlbumInterface(RestInterface):
    name = 'albums'
    model = Album 
    queryable_fields = ['pk', 'artist', 'name', 'released',]
    return_fields = ['pk', 'name', 'released',]
    allowed_queries = ['exact', 'gt', 'lt', 'contains', 'startswith']
    paginate = 15

class TrackInterface(RestInterface):
    name = 'tracks'
    model = Track 
    queryable_fields = ['pk', 'name', 'album',]
    return_fields = ['pk', 'name', 'album',]
    allowed_queries = ['exact', 'gt', 'lt', 'contains', 'startswith']
    paginate = 15
    def get_album(self, obj, iface):
        return obj.album.name


simplerest.root.register(ArtistInterface)
simplerest.root.register(ChartInterface)
simplerest.root.register(AlbumInterface)
simplerest.root.register(TrackInterface)

