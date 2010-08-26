from django.contrib.auth.models import User
from django.test import TestCase
from radio.station.models import Schedule, Spot, DJ, Show
import random
import datetime

def create_dj():
    user = User.objects.create(
            username='rand-%d'%random.randint(1,100)
    )
    dj = DJ.objects.create(
            user=user,
            slug=user.username,
            display_name=user.username,
            summary="test",
            description="test"
    )
    return dj

def create_show(special=False):
    random_name = 'rand-%d'%random.randint(1,100)
    return Show.objects.create(
        name=random_name,
        slug=random_name,
        special_program=special,
        date_added=datetime.datetime.now(),
        image='/fake/ping.png',
        blurb='test',
        description='test'
    )

def create_week_of_spots(when, per_day=1):
    schedule = Schedule.objects.create(start_date=(when-datetime.timedelta(days=14)).date(), end_date=(when+datetime.timedelta(days=14)).date())
    show = create_show()
    dj = create_dj()

    create_spot = lambda offset, day: Spot.objects.create(
        offset=offset,
        repeat_every=Spot.REPEAT_CHOICES_DICT['Weekly'],
        day_of_week=day,
        show=show,
        dj=dj,
        schedule=schedule
    )
    return [create_spot(j, i) for j in range(0, 86400, 86400/per_day) for i in range(0, 7)] 

