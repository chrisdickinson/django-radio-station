from django.test import TestCase
from django.http import Http404
from models import Event, Location
from views import *
from templatetags.radio_events_calendar import calendar_block_generator
import datetime
import calendar

class TestViewContext(TestCase):
    def setUp(self):
        self.today = datetime.datetime.now().date()
        self.location = Location.objects.create(name='test location',
                                                slug='test-location',
                                                blurb='this is a test location',
        )
        self.event = Event.objects.create(name="test event", 
                                    slug="test-event",
                                    weight=0,
                                    blurb="Test event",
                                    content="Test event",
                                    date=self.today,
                                    time_start=datetime.time(2,0),
                                    time_end=datetime.time(3,0)
                            )
        self.event.save()

    def tearDown(self):
        self.event.delete()

    def test_detail_404s(self):
        fake_request = {}
        tomorrow = self.today + datetime.timedelta(days=1)
        self.assertRaises(Http404, event_detail_context, fake_request, 'not-exists', self.today.year, self.today.month, self.today.day)
        self.assertRaises(Http404, event_detail_context, fake_request, self.event.slug, tomorrow.year, tomorrow.month, tomorrow.day)

    def test_detail_context(self):
        self.assertEqual(self.event, event_detail_context({}, 'test-event', self.today.year, self.today.month, self.today.day)['event'])

    def test_events_for_day_context(self):
        from django.db.models.query import QuerySet
        context_1 = events_for_day_context({}, self.today.year, self.today.month, self.today.day)
        context_2 = events_for_day_context({})
        self.assertTrue('events' in context_1)
        self.assertTrue('events' in context_2)
        self.assertTrue('day' in context_1)
        self.assertTrue('day' in context_2)
        self.assertTrue(isinstance(context_1['events'], QuerySet))
        self.assertTrue(isinstance(context_2['events'], QuerySet))
        self.assertEqual(self.today, context_1['day'])
        self.assertEqual(self.today, context_2['day'])

    def test_events_for_location_context_404s(self):
        self.assertRaises(Http404, events_for_location_context, {}, 'dne')

    def test_events_for_location_context(self):
        from django.db.models.query import QuerySet
        context = events_for_location_context({}, self.location.slug)
        self.assertTrue('events' in context)
        self.assertTrue('location' in context)
        self.assertTrue(isinstance(context['events'], QuerySet))
        self.assertTrue(isinstance(context['location'], Location))

    def test_calendar_block_generator(self):
        cal = calendar.monthcalendar(self.today.year, self.today.month)
        gen_cal = calendar_block_generator(self.today)
        gen_cal = [[tup for tup in week] for week in gen_cal]
        self.assertEqual(len(cal), len(gen_cal))
        for cal_week, gen_cal_week in zip(cal, gen_cal):
            self.assertEqual(len(cal_week), len(gen_cal_week))
            for cal_day, gen_cal_tup in zip(cal_week, gen_cal_week):
                self.assertEqual(cal_day, gen_cal_tup[0])
                if cal_day == self.today.day:
                    self.assertTrue(gen_cal_tup[1])

