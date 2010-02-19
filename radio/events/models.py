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
    blurb = models.TextField()

    def __unicode__(self):
        return u"%s" % self.name

    class Meta:
        ordering = ['name']

class Event(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    weight = models.IntegerField(null=True, blank=True, default=0,
        help_text="likelihood that this event will be highlighted. The bigger the number, the more likely.")
    location = models.ForeignKey(Location, null=True, blank=True)
    blurb = models.TextField()
    content = models.TextField()
    date = models.DateField()
    time_start = models.TimeField()
    time_end = models.TimeField(null=True, blank=True)

    def get_absolute_url(self):
        return reverse('event-detail', kwargs = {
            'year':self.date.year,
            'month':self.date.month,
            'day':self.date.day,
            'slug':self.slug
        })

    def __unicode__(self):
        return u"%s" % self.name

    class Meta:
        ordering = ['-date', '-time_start']
