from django.db import models
from django.conf import settings

class Artist(models.Model):
    name = models.CharField(max_length=255)
    def __unicode__(self):
        return self.name
    class Meta:
        ordering=['name']

class Label(models.Model):
    name = models.CharField(max_length=255)
    def __unicode__(self):
        return self.name
    class Meta:
        ordering=['name']

class Album(models.Model):
    name = models.CharField(max_length=255)
    artist = models.ForeignKey(Artist)
    def __unicode__(self):
        return '%s' % (self.name)
    class Meta:
        ordering=['name']

class Track(models.Model):
    name = models.CharField(max_length=255)
    album = models.ForeignKey(Album)
    def __unicode__(self):
        return self.name
    class Meta:
        ordering=['name']

class Genre(models.Model):
    name = models.CharField(max_length=255)
    def __unicode__(self):
        return u"%s" % self.name
