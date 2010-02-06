from django.test import TestCase
from radio.station.schedule.generators import spot_generate_dicts, spot_generate_objects
from radio.station.schedule.exceptions import BadSpotIncrement, BadSpotOffset

class GeneratorTests(TestCase):
    def test_spot_generate_dicts(self):
        increment = 60 * 60 * 3 # three hour increment
        dicts = spot_generate_dicts(increment)

        day_cusp = 24/3

        should_equal = 7 * day_cusp   # should equal seven days times (24 hours divided by three hour blocks)
        self.assertEqual(len(dicts), should_equal)
        self.assertTrue('offset' in dicts[0].keys())
        self.assertTrue('repeat_every' in dicts[0].keys())
        self.assertTrue('day_of_week' in dicts[0].keys())
        self.assertTrue('show_pk' in dicts[0].keys())
        self.assertTrue('dj_pk' in dicts[0].keys())
        for i in range(0,7):
            self.assertEqual(dicts[i*day_cusp+1]['offset']-dicts[i*day_cusp]['offset'], increment)              #next dict in list should have an offset of the last dict plus increment
            if i != 0:
                self.assertEqual(dicts[i*day_cusp]['day_of_week'] - dicts[i*day_cusp-1]['day_of_week'], 1)      #see if we're incrementing day_of_week correctly
    
    def test_fail_on_bad_increment(self):
        increment = 0 # zero second increment
        negative_increment = -1 #negative one second increment
        self.assertRaises(BadSpotIncrement, spot_generate_dicts, increment)
        self.assertRaises(BadSpotIncrement, spot_generate_dicts, negative_increment)

