from django.test import TestCase
from radio_logs.views import time_to_ceiling, date_radius, time_context

class TestTimeToCeiling(TestCase):
    def test_requires_datetime(self):
        self.assertRaises(AttributeError, time_to_ceiling, {}, 3.0)

    def test_within_datetime_bounds(self):
        from datetime import datetime, timedelta
        bound_low = datetime(2009, 11, 1, 0, 0)
        bound_high = datetime(2009, 11, 1, 23, 59)
        try:
            self.assertEqual(time_to_ceiling(bound_low, 3.0).hour, 3) 
            self.assertEqual(time_to_ceiling(bound_high, 3.0).hour, 23)
            self.assertEqual(time_to_ceiling(bound_high, 3.0).minute, 59)
        except ValueError, e:
            self.fail()

    def test_returns_predicted_time(self):
        from datetime import datetime
        test_values = (
             3, 3, 3,          # [0-2] -> 3 
             6, 6, 6,          # [3-5] -> 6
             9, 9, 9,          # [6-8] -> 9
            12,12,12,          # [8-11] -> 12
            15,15,15,          # [12-14] -> 15
            18,18,18,          # ... 
            21,21,21,
            23,23,23, 
        )
        for (_out, _in) in zip(test_values, range(0, 24)):
            when = datetime(2009, 11, 1, _in, 0)
            self.assertEqual(time_to_ceiling(when, 3.0).hour, _out)

class TestDateRadius(TestCase):
    def test_length_works(self):
        from datetime import datetime, timedelta
        now = datetime.now()
        cap = datetime.now() + timedelta(days=4)
        for i in range(0, 4):
            results = date_radius(now, i, cap)
            self.assertEqual(1 + i*2, len(results))

    def test_in_order(self):
        from datetime import datetime, timedelta
        from copy import copy
        now = datetime.now()
        cap = datetime.now() + timedelta(days=4)
        results = date_radius(now, 2, cap)
        original_results = copy(results)
        results.sort()
        self.assertEqual(results, original_results)

    def test_flattens_date(self):
        from datetime import datetime, timedelta
        now = datetime.now()
        cap = datetime.now() + timedelta(days=4)
        results = date_radius(now, 2, cap, (0, 30))
        for i in results:
            self.assertEqual((i.hour, i.minute), (0, 30))

        results = date_radius(now, 2, cap)
        for i in results:
            self.assertEqual((i.hour, i.minute), (0, 0))

    def test_approaches_cap(self):
        from datetime import datetime, timedelta
        now = datetime.now()
        cap = datetime.now() + timedelta(days=2)
        results = date_radius(now, 4, cap)
        self.assertEqual(results[-1].date(), cap.date())
        self.assertEqual(results[0].date(), cap.date() - timedelta(days=8))

class TestTimeContext(TestCase):
    def test_404_on_invalid_time(self):
        from datetime import datetime, timedelta
        from django.http import Http404
        invalid_time = datetime.now() + timedelta(days=1)
        self.assertRaises(Http404, time_context, {}, *invalid_time.timetuple()[:5])

    def test_when_is_automatically_now(self):
        from datetime import datetime, timedelta
        fake_request = {}
        ctxt = time_context(fake_request)
        now = datetime.now()
        self.assertEqual((now.hour, now.minute), (ctxt['when'].hour, ctxt['when'].minute))
        self.assertEqual((now.hour, now.minute), (ctxt['now'].hour, ctxt['now'].minute))

    def test_assert_proper_types(self):
        from datetime import datetime
        from django.db.models.query import QuerySet
        from itertools import izip
        fake_request = {}
        ctxt = time_context(fake_request)
        self.assertTrue(isinstance(ctxt['logs'], QuerySet))
        self.assertTrue(isinstance(ctxt['time_range'], izip))
        self.assertTrue(hasattr(ctxt['date_range'], 'next'))
        for i in ('when', 'now', 'prev_time'):
            self.assertTrue(isinstance(ctxt[i], datetime))
        self.assertTrue(isinstance(ctxt['next_time'], (datetime, type(None))))
