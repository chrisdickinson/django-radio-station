from django.core.urlresolvers import reverse
from django.test import TestCase
from radio.datetime import datetime_to_ceiling, generate_datetime_radius
from radio.logs.views import time_view

class TestTimeToCeiling(TestCase):
    def test_requires_datetime(self):
        self.assertRaises(AttributeError, datetime_to_ceiling, {}, 3.0)

    def test_within_datetime_bounds(self):
        from datetime import datetime, timedelta
        bound_low = datetime(2009, 11, 1, 0, 0)
        bound_high = datetime(2009, 11, 1, 23, 59)
        try:
            self.assertEqual(datetime_to_ceiling(bound_low, 3.0).hour, 3) 
            self.assertEqual(datetime_to_ceiling(bound_high, 3.0).hour, 23)
            self.assertEqual(datetime_to_ceiling(bound_high, 3.0).minute, 59)
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
            self.assertEqual(datetime_to_ceiling(when, 3.0).hour, _out)

class TestDateRadius(TestCase):
    def test_length_works(self):
        from datetime import datetime, timedelta
        now = datetime.now()
        for i in range(0, 4):
            results = generate_datetime_radius(now, i)
            self.assertEqual(1 + i*2, len(results))

    def test_in_order(self):
        from datetime import datetime, timedelta
        from copy import copy
        now = datetime.now()
        results = generate_datetime_radius(now, 2)
        original_results = copy(results)
        results.sort()
        self.assertEqual(results, original_results)

    def test_flattens_date(self):
        from datetime import datetime, timedelta
        now = datetime.now()
        cap = datetime.now() + timedelta(days=4)
        results = generate_datetime_radius(now, 2, (0, 30))
        for i in results:
            self.assertEqual((i.hour, i.minute), (0, 30))

        results = generate_datetime_radius(now, 2)
        for i in results:
            self.assertEqual((i.hour, i.minute), (0, 0))

class TestTimeContext(TestCase):
    def test_404_on_invalid_time(self):
        from datetime import datetime, timedelta
        from django.http import Http404

        invalid_time = datetime.now() + timedelta(days=1)
        kwargs = {
            'year':invalid_time.year,
            'month':invalid_time.strftime('%b'),
            'day':invalid_time.day,
            'hour':invalid_time.hour,
        }
        response = self.client.get(reverse('logs-time', kwargs=kwargs))
        self.assertEqual(response.status_code, 404)

    def test_when_is_automatically_now(self):
        from datetime import datetime, timedelta
        now = datetime.now()
        response = self.client.get(reverse('logs-time-now'))
        ctxt = response.context
        self.assertEqual((now.hour, now.minute), (ctxt['current_datetime'].hour, ctxt['current_datetime'].minute))
