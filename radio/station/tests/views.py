from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test import TestCase
from radio.station.models import Schedule, Spot, DJ, Show
from .test_utils import create_show, create_dj, create_week_of_spots
import random
import datetime

class TestOfViews(TestCase):
    def test_for_day_returns_weekday_schedule(self):
        now = datetime.datetime.now()
        day_of_week_to_test = random.randint(1,6)
        num_spots = random.randint(1,6)
        spots = create_week_of_spots(now, num_spots)
        response = self.client.get(reverse('for-day', kwargs={'day_of_week':day_of_week_to_test}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['weekday'], day_of_week_to_test)
        self.assertEqual(len(response.context['spots']), num_spots)
        self.assertEqual(
            [spot.pk for spot in response.context['spots']], 
            [spot.pk for spot in spots if spot.day_of_week == day_of_week_to_test])

    def test_for_day_returns_404_on_bad_weekday(self):
        now = datetime.datetime.now()
        day_of_week_to_test = random.randint(7,9)
        num_spots = random.randint(1,6)
        spots = create_week_of_spots(now, num_spots)
        response = self.client.get(reverse('for-day', kwargs={'day_of_week':day_of_week_to_test}))
        self.assertEqual(response.status_code, 404)

    def test_for_day_returns_404_on_no_schedule(self):
        day_of_week_to_test = random.randint(0,6)
        response = self.client.get(reverse('for-day', kwargs={'day_of_week':day_of_week_to_test}))
        self.assertEqual(response.status_code, 404)

    def test_show_detail_returns_show_from_slug(self):
        now = datetime.datetime.now()
        day_of_week_to_test = random.randint(1,6)
        num_spots = random.randint(1,6)
        spots = create_week_of_spots(now, num_spots)
        random_spot = spots[random.randint(0, len(spots)-1)]
        random_spot.show = create_show()
        random_spot.show.slug = 'random-spot-%d'%random.randint(0,100)
        random_spot.show.save()
        slug = random_spot.show.slug
        response = self.client.get(reverse('show-detail', kwargs={
            'show_slug':slug
        })) 
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['show'].pk, random_spot.show.pk)

    def test_show_detail_returns_404_on_no_schedule(self):
        show = create_show()
        show.slug = 'random-show-%d'%random.randint(0,100)
        show.save()
        response = self.client.get(reverse('show-detail', kwargs={'show_slug':show.slug}))
        self.assertEqual(response.status_code, 404)

    def test_show_detail_returns_404_on_nonexistant_show(self):
        now = datetime.datetime.now()
        day_of_week_to_test = random.randint(1,6)
        num_spots = random.randint(1,6)
        spots = create_week_of_spots(now, num_spots)
        bad_slug = 'bad-slug-%d'%random.randint(0,100)
        response = self.client.get(reverse('show-detail', kwargs={'show_slug':bad_slug}))
        self.assertEqual(response.status_code, 404)

    def test_dj_detail_returns_dj_from_slug(self):
        now = datetime.datetime.now()
        day_of_week_to_test = random.randint(1,6)
        num_spots = random.randint(1,6)
        spots = create_week_of_spots(now, num_spots)
        random_spot = spots[random.randint(0, len(spots)-1)]
        random_spot.dj = create_dj()
        random_spot.dj.slug = 'random-spot-%d'%random.randint(0,100)
        random_spot.dj.save()
        slug = random_spot.dj.slug
        response = self.client.get(reverse('dj-detail', kwargs={
            'dj_slug':slug
        })) 
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['dj'].pk, random_spot.dj.pk)

    def test_dj_detail_returns_404_on_no_schedule(self):
        dj = create_dj()
        dj.slug = 'random-dj-%d'%random.randint(0,100)
        dj.save()
        response = self.client.get(reverse('dj-detail', kwargs={'dj_slug':dj.slug}))
        self.assertEqual(response.status_code, 404)

    def test_dj_detail_returns_404_on_nonexistant_dj(self):
        now = datetime.datetime.now()
        day_of_week_to_test = random.randint(1,6)
        num_spots = random.randint(1,6)
        spots = create_week_of_spots(now, num_spots)
        bad_slug = 'bad-slug-%d'%random.randint(0,100)
        response = self.client.get(reverse('dj-detail', kwargs={'dj_slug':bad_slug}))
        self.assertEqual(response.status_code, 404)
