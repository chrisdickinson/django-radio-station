from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from radio.station.models import DJ
from radio.logs.models import Entry
from .tasks import post_responses
import datetime

class Request(models.Model):
    from_user = models.ForeignKey(User)
    artist_name = models.CharField(max_length=255)
    track_name = models.CharField(max_length=255)
    published = models.DateTimeField(auto_now_add=True)
    fulfilled_by = models.ForeignKey(DJ, null=True, blank=True)

    def __unicode__(self):
        return u'%s requested "%s - %s"' % (from_user.get_full_name(), artist_name, track_name)

def create_entry(sender, **kwargs):
    entry = kwargs.get('instance', None)
    if entry:
        artist_name, track_name = entry.artist.name, entry.track.name
        now = datetime.datetime.now()
        requests = Request.objects.filter(published__gte=now-datetime.timedelta(days=3), fulfilled_by__isnull=True, artist_name=artist_name, track_name=track_name)
        requests.update(fulfilled_by=entry.dj)
        post_responses(requests)

post_save.connect(create_entry, sender=Entry)
