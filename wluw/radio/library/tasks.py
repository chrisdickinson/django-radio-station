from wluw.radio.library.models import Album 
from django.conf import settings
from waiter import Waiter
from celery.decorators import task
from wluw.radio.logs.models import Entry

@task
def ping_nodejs_with(entry_pk):
    if entry_pk:
        try:
            entry = Entry.objects.get(pk=entry_pk)        
            waiter = Waiter()
            show_name = 'Rotation'
            try:
                show_name = entry.show.name
            except:
                pass 

            waiter/("http://127.0.0.1:%d"%settings.NODE_PORT)/{
                'artist':entry.artist.name,
                'album':entry.album.name,
                'track':entry.track.name,
                'show':show_name,
                'dj':str(entry.dj),
                'when':str(entry.submitted),
                'image':entry.album.image_large,
            }   
        except Entry.DoesNotExist:
            pass
@task
def grab_album_art(album_pk, from_log_pk=None):
    try:
        album = Album.objects.get(pk=album_pk)
    except Album.DoesNotExist:
        ping_nodejs_with(from_log_pk)
    else:
        Album.objects.filter(pk=album_pk).update(status=Album.Status.WORKING)
        waiter = Waiter()
        try: 
            result = waiter/'http://ws.audioscrobbler.com/2.0/'/{
                'method':'album.getinfo',
                'api_key':settings.LASTFM_API_KEY,
                'artist':album.artist.name,
                'album':album.name,
                'format':'json'
            }
            if result.get('error', None):
                raise Exception()
            images = dict([(image['size'], image['#text']) for image in result['album']['image']])

            album.lastfm_url = result['album']['url']

            album.image_large = images.get('large', '')
            album.image_medium = images.get('medium', '')
            album.image_small = images.get('small', '')

            album.mdid = result['album']['mbid']
            album.status = Album.Status.OKAY

            album.save()
            ping_nodejs_with(from_log_pk)
        except Exception, e:
            Album.objects.filter(pk=album_pk).update(status=Album.Status.PENDING)
            ping_nodejs_with(from_log_pk)


