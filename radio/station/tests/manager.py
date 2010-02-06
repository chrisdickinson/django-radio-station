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

class TestOfSpotManager(TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_get_current_spot_gets_current_spot(self):
        now = datetime.datetime.now()
        seven_days = datetime.timedelta(days=7)
        schedule = Schedule.objects.create(start_date=(now-seven_days).date(), end_date=(now+seven_days).date())
        spot = Spot.objects.create(
            day_of_week=now.weekday(),
            repeat_every=Spot.REPEAT_CHOICES_DICT['Weekly'],
            offset=0,
            dj=create_dj(),
            show=create_show(),
            schedule=schedule
        )
        results = Spot.objects.get_current_spot(now)
        self.assertEqual(spot.pk, results.pk)

    def test_get_current_spot_gets_spot_from_current_schedule(self):
        now = datetime.datetime.now()
        seven_days = datetime.timedelta(days=7)
        schedule_one = Schedule.objects.create(start_date=(now-seven_days).date(), end_date=(now+seven_days).date())
        schedule_two = Schedule.objects.create(start_date=(now-seven_days-seven_days).date(), end_date=(now+seven_days+seven_days))
        spot = Spot.objects.create(
            day_of_week=now.weekday(),
            repeat_every=Spot.REPEAT_CHOICES_DICT['Weekly'],
            offset=0,
            dj=create_dj(),
            show=create_show(),
            schedule=schedule_one
        )
        results = Spot.objects.get_current_spot(now)
        self.assertEqual(spot.schedule.pk, results.schedule.pk)

    def test_get_current_spot_will_return_nonweekly_repeat(self):
        now = datetime.datetime.now()
        seven_days = datetime.timedelta(days=7)
        schedule_one = Schedule.objects.create(start_date=(now-seven_days).date(), end_date=(now+seven_days).date())
        to_offset = lambda x: x.hour*3600 + x.minute*60 + x.second
        spot = Spot.objects.create(
            day_of_week=now.weekday(),
            repeat_every=Spot.REPEAT_CHOICES_DICT['Weekly'],
            offset=to_offset(now) + 1,
            dj=create_dj(),
            show=create_show(),
            schedule=schedule_one
        )
        nth_of_month = (now.day / 7) + 1
        different_repeat = Spot.objects.create(
            day_of_week=now.weekday(),
            repeat_every=nth_of_month,
            offset=to_offset(now)-1,
            dj=create_dj(),
            show=create_show(),
            schedule=schedule_one

        )
        results = Spot.objects.get_current_spot(now)
        self.assertEqual(results.pk, different_repeat.pk)

    def test_get_current_spot_raises_when_no_schedule_is_available(self):
        now = datetime.datetime.now()
        self.assertRaises(Schedule.DoesNotExist, Spot.objects.get_current_spot, now)

    def test_get_current_spot_raises_if_day_is_empty(self):
        now = datetime.datetime.now()
        tomorrow_day = (now+datetime.timedelta(days=1)).weekday()
        spot = Spot.objects.create(
            day_of_week=tomorrow_day,
            repeat_every=Spot.REPEAT_CHOICES_DICT['Weekly'],
            offset=0,
            dj=create_dj(),
            show=create_show(),
            schedule=Schedule.objects.create(start_date=now.date(), end_date=(now+datetime.timedelta(days=1)).date())
        )
        self.assertRaises(Spot.DoesNotExist, Spot.objects.get_current_spot, now)

    def test_filter_next_spots_for_week(self):
        now = datetime.datetime.now()
        if now.weekday() == 6:
            now = now - datetime.timedelta(days=1)

        spots = create_week_of_spots(now)
        next_spots = Spot.objects.filter_next_spots_for_week(now)
        next_spots_unpacked = [i for i in next_spots]
        self.assertEqual(next_spots_unpacked[-1].pk, spots[-1].pk)
        self.assertEqual(next_spots_unpacked[-1].day_of_week, 6)
        self.assertEqual(next_spots[0].day_of_week, now.weekday()+1)

    def test_filter_next_spots_for_week_grabs_spots_today_if_after_offset(self):
        now = datetime.datetime.now()
        to_offset = lambda x: x.hour*3600 + x.minute*60 + x.second
        if now.weekday() == 6:
            now = now - datetime.timedelta(days=1)

        spots = create_week_of_spots(now)
        next_spot_today = Spot.objects.create(
            day_of_week=now.weekday(),
            repeat_every=Spot.REPEAT_CHOICES_DICT['Weekly'],
            offset=to_offset(now)+10,
            dj=spots[0].dj,
            show=spots[0].show,
            schedule=spots[0].schedule
        )
        next_spots = Spot.objects.filter_next_spots_for_week(now)
        next_spots_unpacked = [i for i in next_spots]
        self.assertEqual(next_spots[0].day_of_week, now.weekday())
        self.assertEqual(next_spots[0].pk, next_spot_today.pk)

    def test_next_spots(self):
        now = datetime.datetime.now()
        to_offset = lambda x: x.hour*3600 + x.minute*60 + x.second
        if now.weekday() == 6:
            now = now - datetime.timedelta(days=1)
        spots = create_week_of_spots(now)
        next_spots = [i for i in Spot.objects.next_spots(now)]
        self.assertEqual(next_spots[0].day_of_week, now.weekday()+1)
        self.assertEqual(next_spots[-1].day_of_week, 6)
        
        spots_until_monday = 6 - now.weekday()
        self.assertEqual(next_spots[spots_until_monday].day_of_week, 0)
        self.assertEqual(len(next_spots), spots_until_monday+len(spots))

    def test_for_day(self):
        now = datetime.datetime.now()
        spots = create_week_of_spots(now, per_day=random.randint(1,6))
        when = now - datetime.timedelta(days=now.weekday())
        for i in range(0, 6):
            has_correct_day = lambda spot: spot.day_of_week==i
            spots_for_day = Spot.objects.for_day(when)
            when += datetime.timedelta(days=1)
            self.assertTrue(all((has_correct_day(spot) for spot in spots_for_day)))

    def test_for_week(self):
        now = datetime.datetime.now()
        spots = create_week_of_spots(now, per_day=random.randint(1,6))
        when = now - datetime.timedelta(days=now.weekday())
        unpacked_week = [spot for spot in Spot.objects.for_week(when)]
        self.assertEqual(spots, unpacked_week) 

    def test_for_day_includes_nonweekly(self):
        print ""
        print """
            **** `test_for_day_includes_nonweekly` stubbed!
        """.strip()
        pass

class TestOfScheduleManager(TestCase):
    def test_of_get_current_schedule_returns_current_schedule(self):
        now = datetime.datetime.now()
        sched = Schedule.objects.create(start_date=now.date(), end_date=now.date())
        self.assertEqual(Schedule.objects.get_current_schedule(now), sched) 

    def test_of_get_current_schedule_prefers_smallest_schedule(self):
        now = datetime.datetime.now()
        sched = Schedule.objects.create(start_date=now.date(), end_date=now.date())
        big_sched = Schedule.objects.create(start_date=(now-datetime.timedelta(days=7)).date(),
                                            end_date=(now+datetime.timedelta(days=7)).date())
        self.assertEqual(Schedule.objects.get_current_schedule(now), sched)

    def test_of_get_current_schedule_raises_on_no_schedule(self):
        self.assertRaises(Schedule.DoesNotExist, Schedule.objects.get_current_schedule, datetime.datetime.now())
