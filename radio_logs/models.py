from django.db import models
from d51_admin_autofk import fields as d51fields
from radio_library.models import Artist, Album, Track, Genre
from radio_station.models import DJ, Show

def instant_artist(widget, data, name):
    value = data.get(name, None)
    if value is not None and value != '':
        (obj, created) = widget.model.objects.get_or_create(name=value)
        value = obj.pk
    return value 

def instant_album(widget, data, name):
    value = data.get(name, None)
    artist_value = data.get('artist', None)
    if value is not None and artist_value is not None and value != '' and artist_value != '':
        artist = Artist.objects.get(name__exact=artist_value)
        (obj, created) = widget.model.objects.get_or_create(name=value, artist=artist)
        value = obj.pk
    return value 

def instant_track(widget, data, name):
    value = data.get(name, None)
    artist_value = data.get('artist', None)
    album_value = data.get('album', None)
    if value is not None and value != '':
        if artist_value is not None and artist_value != '':
            artist = Artist.objects.get(name__exact=artist_value)
            (album, created) = Album.objects.get_or_create(name="Unknown Album", artist=artist)
            if album_value is not None and album_value != '':
                album = Album.objects.get(name__exact=album_value, artist=artist)
            (track, created) = widget.model.objects.get_or_create(name=value, album=album)
            value = track.pk
        else:
            value = None
    return value 

class Request(models.Model):
    what = models.CharField(max_length=255)
    when = models.DateTimeField(auto_now_add=True)
    who = models.CharField(max_length=255, null=True, blank=True)
    ip = models.IPAddressField()

class Entry(models.Model):
    artist = d51fields.ForeignKey(Artist, instantiate_fn=instant_artist)
    album = d51fields.ForeignKey(Album, instantiate_fn=instant_album)
    track = d51fields.ForeignKey(Track, instantiate_fn=instant_track)
    genre = models.ForeignKey(Genre)
    submitted = models.DateTimeField(auto_now_add=True)
    is_rotation = models.BooleanField()
    dj = models.ForeignKey(DJ)
    show = models.ForeignKey(Show, null=True, blank=True)
    def __unicode__(self):
        return "%s [%s]" % (self.artist, self.track)
    class Meta:
        verbose_name = "entry"
        verbose_name_plural = "entries"

