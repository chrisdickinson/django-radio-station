from django.db import models

class Artist(models.Model):
    name = models.CharField(max_length=255)
    def __unicode__(self):
        return self.name
    class Meta:
        ordering=['name']
        db_table = 'radio_library_artist'

class Label(models.Model):
    name = models.CharField(max_length=255)
    def __unicode__(self):
        return self.name
    class Meta:
        ordering=['name']
        db_table = 'radio_library_label'

class Album(models.Model):
    name = models.CharField(max_length=255)
    artist = models.ForeignKey(Artist)
    def __unicode__(self):
        return '%s' % (self.name)
    class Meta:
        ordering=['name']
        db_table = 'radio_library_album'

class Track(models.Model):
    name = models.CharField(max_length=255)
    album = models.ForeignKey(Album)
    def __unicode__(self):
        return self.name
    class Meta:
        ordering=['name']
        db_table = 'radio_library_track'

class Genre(models.Model):
    name = models.CharField(max_length=255)
    def __unicode__(self):
        return u"%s" % self.name

    class Meta:
        db_table = 'radio_library_genre'
