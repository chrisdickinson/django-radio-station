from django.db import models
from d51_admin_autofk import fields as d51fields
from radio.library.models import Artist, Album, Track, Genre
from radio.station.models import DJ, Show
from .managers import EntryManager

def instant_artist(widget, data, name):
    value = data.get(name, None)
    if value is not None and value != '':
        (obj, created) = widget.model.objects.get_or_create(name=value)
        value = obj
    return value 

def instant_album(widget, data, name):
    value = data.get(name, None)
    artist_value = data.get('artist', None)
    if value is not None and artist_value is not None and value != '' and artist_value != '':
        artist = Artist.objects.get(name__exact=artist_value)
        (obj, created) = widget.model.objects.get_or_create(name=value, artist=artist)
        value = obj
    return value 

def instant_track(widget, data, name):
    value = data.get(name, None)
    artist_value = data.get('artist', None)
    album_value = data.get('album', None)
    if value is not None and value != '':
        if artist_value is not None and artist_value != '':
            artist = Artist.objects.get(name__exact=artist_value)
            (album, created) = Album.objects.get_or_create(name="<Untitled Album>", artist=artist)
            if album_value is not None and album_value != '':
                try:
                    album = Album.objects.filter(name__exact=album_value, artist=artist)[0]
                except IndexError:
                    pass
            (track, created) = widget.model.objects.get_or_create(name=value, album=album)
            value = track
        else:
            value = None
    return value 

class Entry(models.Model):
    artist = d51fields.ForeignKey(Artist, instantiate_fn=instant_artist)
    album = d51fields.ForeignKey(Album, js_methods=['match_artist_and_startswith'], instantiate_fn=instant_album)
    track = d51fields.ForeignKey(Track, js_methods=['match_album_and_startswith'], instantiate_fn=instant_track)
    genre = models.ForeignKey(Genre)
    submitted = models.DateTimeField(auto_now_add=True)
    is_rotation = models.BooleanField()
    dj = models.ForeignKey(DJ)
    show = models.ForeignKey(Show, null=True, blank=True)
    objects = EntryManager()
    def __unicode__(self):
        return "%s [%s]" % (self.artist, self.track)
    class Meta:
        verbose_name = "entry"
        verbose_name_plural = "entries"
