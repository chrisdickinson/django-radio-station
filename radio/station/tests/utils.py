from django.test import TestCase
from radio.datetime import *
from radio.station.utils import *
import datetime

class TestUtilityFunctions(TestCase):
    def test_get_offset_in_seconds(self):
        dtime = datetime.datetime(2009, 11, 1, 2, 30)
        expected_seconds = 2*(60**2) + 30*60
        self.assertEqual(expected_seconds, get_offset_in_seconds(dtime))
        self.assertEqual(0, get_offset_in_seconds(strip_hour_and_minute(dtime)))
        self.assertEqual(0, get_offset_in_seconds(dtime.date()))

    def test_get_offset_in_seconds_fail(self):
        self.assertRaises(AttributeError, get_offset_in_seconds, 2)

    def test_get_start_of_week(self):
        known_start_of_week = datetime.datetime(2009, 11, 30)
        dtime = datetime.datetime(2009,12,1)
        self.assertEqual(known_start_of_week, get_start_of_week(dtime))

    def test_get_week_range(self):
        known_start_of_week = datetime.datetime(2009, 11, 30)
        dtime = datetime.datetime(2009,12,1)
        week_range = get_week_range(dtime)
        week_range = [date for date in week_range]
        self.assertEqual(7, len(week_range))
        self.assertEqual(known_start_of_week.date(), week_range[0])
        self.assertEqual((known_start_of_week+datetime.timedelta(days=6)).date(), week_range[-1])

    def test_get_day_of_week(self):
        dtime = datetime.datetime(2009, 12, 1)      # <- a tuesday
        expected = datetime.datetime(2009, 12, 2)   # <- a wednesday
        expected_2 = datetime.datetime(2009, 11, 29)
        self.assertEqual(expected, get_day_of_week(2, dtime))
        self.assertEqual(expected_2, get_day_of_week(-1, dtime))    # get the sunday of the week previous

class TestChainedQueryset(TestCase):

    def test_get_slice(self):
        sets = [
            [1,2,3],
            [4,5],
            [6,7,8],
        ]
        cqs = ChainedQuerySet(*sets)
        self.assertEqual(cqs[0:], [1,2,3,4,5,6,7,8])
        self.assertEqual(cqs[2:4], [3,4])
        self.assertEqual(cqs[:2], [1,2])
        self.assertRaises(IndexError, cqs.__getitem__, slice(-2)) 
        self.assertEqual([], cqs[200:])
    def test_get_index(self):
        sets = [
            [1,2,3,4],
            [5,6,7,8],
        ]
        cqs = ChainedQuerySet(*sets)
        self.assertEqual(5, cqs[4])
        self.assertEqual(3, cqs[2])

    def test_get_negative_index(self):
        sets = [
            [1,2,3,4],
            [5,6,7,8],
        ]
        cqs = ChainedQuerySet(*sets)
        self.assertRaises(IndexError, cqs.__getitem__, -1)

