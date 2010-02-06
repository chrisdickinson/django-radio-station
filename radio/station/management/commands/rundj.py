from django.core.management.base import BaseCommand, CommandError
from optparse import make_option
import os
import sys
import datetime
import random
class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option('--switch-every', dest='switch_s', default=None, 
            help='Tells Django how often to simulate switching DJs'),
        make_option('--log-every', dest='log_every_s', default=60,
            help='Tells Django how often to simulate logging music'),
        make_option('--random-rotation', action='store_true', dest='random_rotation', default=False,
            help='Tells Django to randomly select cuts as "rotation" music.'),
        make_option('--fulfill-requests', action='store_true', dest='fulfill_requests', default=False,
            help='Tells Django to randomly fulfill requests.')

    )

    def handle(self, *args, **options):

        def inner_run(func):
            print "Starting fake-dj..."
            initial = datetime.datetime.now()
            while True:
                now = datetime.datetime.now()
                delta = now - initial
                func(delta.microseconds)
                initial = now

        from radio.logs.models import Entry
        from radio.library.models import Track, Genre
        from radio.station.models import DJ
        total_tracks = 300000#len(Track.objects.all())
        log_every_s = options.get('log_every_s', 60) * 1000000
        switch_s = options.get('switch_s', None)
        self.last_log = 0

        def log_function(delta_seconds, entry_kwargs={}):
            self.last_log += delta_seconds
            if self.last_log > log_every_s:
                self.last_log = 0
                track = None
                while track is None:
                    try:
                        random_pk = int(random.random() * total_tracks) 
                        track = Track.objects.get(pk=random_pk)
                    except:
                        pass
                genre = Genre.objects.all()[0]

                kwargs = {
                    'track':track,
                    'album':track.album,
                    'artist':track.album.artist,
                    'genre':genre,
                }
                kwargs.update(entry_kwargs)
                try:
                    entry = Entry(**kwargs)
                    entry.save()
                    print "Saving %s - %s - %s as %s" % (
                        entry.artist,
                        entry.album,
                        entry.track,
                        entry.dj
                    )
                except Exception, e:
                    print e
                    sys.stderr.write(self.style.ERROR('Error: could not log %s' % str(kwargs)))
                    os._exit(1)

        def random_rotation(func):
            def inner_random_rotation(delta_seconds, entry_kwargs={}):
                kwargs = {}
                is_rotation = int(random.random() * 100) > 50
                if is_rotation:
                    kwargs = {
                        'is_rotation':True
                    }
                kwargs.update(entry_kwargs)
                return func(delta_seconds, kwargs)
            return inner_random_rotation

        dj = DJ.objects.all()[0]
        def switch_dj(func, parent_dj=dj):
            def inner_switch_dj(delta_seconds, entry_kwargs={}, last_switch=0, dj=parent_dj):
                last_switch += delta_seconds
                if switch_s is not None and last_switch > switch_s:
                    try:
                        new_dj = DJ.objects.exclude(pk=dj.pk)[0]
                        dj = new_dj
                    except IndexError:
                        pass
                kwargs = {
                    'dj':dj,
                }
                kwargs.update(entry_kwargs)
                return func(delta_seconds, kwargs)
            return inner_switch_dj
 
        log_function = switch_dj(log_function)
        if options.get('random_rotation', False):
            log_function = random_rotation(log_function)


        try: 
            inner_run(log_function)
        except KeyboardInterrupt:
            print "Stopping rundj..."
