from django.db import models
from django.contrib.localflavor.us.models import * 
from django.conf import settings
from django.core.urlresolvers import reverse

class Location(models.Model):
    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(max_length=255, unique=True)
    address_line_1 = models.CharField(max_length=255, blank=True, null=True)
    address_line_2 = models.CharField(max_length=255, blank=True, null=True)
    state = USStateField(null=True, blank=True)
    zip = models.CharField(max_length=255, null=True, blank=True)
    phone = models.CharField(max_length=255, null=True, blank=True)

    def __unicode__(self):
        return u"%s" % self.name

class Event(models.Model):
    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(max_length=255, unique=True)
    location = models.ForeignKey(Location, null=True, blank=True)
    date = models.DateField()
    time_start = models.TimeField()
    time_end = models.TimeField()

    def get_absolute_url(self):
        return reverse('event-detail', kwargs = {
            'year':self.date.year,
            'month':self.date.month,
            'day':self.date.day,
            'slug':self.slug
        })


    def __unicode__(self):
        return u"%s" % self.name
