from wluw.radio.library.models import Album 
from django.conf import settings
from waiter import Waiter
from celery.decorators import task

@task
def grab_album_art(album_pk):
    try:
        album = Album.objects.get(pk=album_pk)
    except Album.DoesNotExist:
        pass
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

            album.image_large = images.get('large', '')
            album.image_medium = images.get('medium', '')
            album.image_small = images.get('small', '')

            album.mdid = result['album']['mbid']
            album.status = Album.Status.OKAY

            album.save()
        except Exception, e:
            print e
            Album.objects.filter(pk=album_pk).update(status=Album.Status.PENDING)


