from django.db import models

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
    class Status(object):
        PENDING = 0
        WORKING = 1
        OKAY = 2
        ERROR = 3
        values = (
            (0, 'pending'),
            (1, 'working'),
            (2, 'okay'),
            (3, 'error'),
        )
    name = models.CharField(max_length=255)
    artist = models.ForeignKey(Artist)

    lastfm_url = models.CharField(max_length=255, null=True, blank=True)
    image_large = models.CharField(max_length=255, null=True, blank=True)
    image_medium = models.CharField(max_length=255, null=True, blank=True)
    image_small = models.CharField(max_length=255, null=True, blank=True)
    mbid = models.CharField(max_length=36, null=True, blank=True)

    status = models.IntegerField(choices=Status.values, default=Status.PENDING)

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
