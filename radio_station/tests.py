from django.test import TestCase
from schedule.generators import spot_generate_dicts, spot_generate_objects
from schedule.exceptions import BadSpotIncrement, BadSpotOffset
from schedule.controller import ScheduleController

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


class ControllerTests(TestCase):
    def test_modify_spot_offset(self):
        spots = spot_generate_dicts(60*60*3)
        new_fake_post = {
            ScheduleController.ACTION_KEY:'offset',
            ScheduleController.VALUES_KEY:{
                'index':1,
                'value':5400,
            }
        }
        ctrl = ScheduleController(spots, new_fake_post)
        self.assertEqual(ctrl.spots[1]['offset'], 5400)

    def test_delete_spot(self):
        spots = spot_generate_dicts(60*60*3)
        old_len = len(spots)
        new_fake_post = {
            ScheduleController.ACTION_KEY:'delete',
            ScheduleController.VALUES_KEY:{
                'index':1,
            }
        }
        ctrl = ScheduleController(spots, new_fake_post)
        self.assertEqual(old_len - len(ctrl.spots), 1)

    def test_split_and_merge_weeks(self):
        spots = spot_generate_dicts(60*60*3)
        expected_difference = 5             #by splitting a spot into "first week", etc, we should get five new spots
        old_len = len(spots)
        new_fake_post = {
            ScheduleController.ACTION_KEY:'repeat_every',
            ScheduleController.VALUES_KEY:{
                'index':1,
                'value':1,
            }
        }
        ctrl = ScheduleController(spots, new_fake_post)
        self.assertEqual(len(ctrl.spots) - old_len, expected_difference)

        new_fake_post = {
            ScheduleController.ACTION_KEY:'offset',
            ScheduleController.VALUES_KEY:{
                'index':1,
                'value':5400,
            }
        }
        ctrl = ScheduleController(ctrl.spots, new_fake_post)
       
        # assert that, for every spot that is associated with this spot, the offset changed
        for spot in ctrl.spots:
            if spot['day_of_week'] == 0 and spot['repeat_every'] != 0: 
                self.assertEqual(spot['offset'], 5400)

        new_fake_post = {
            ScheduleController.ACTION_KEY:'repeat_every',
            ScheduleController.VALUES_KEY:{
                'index':1,
                'value':0
            }
        }
        ctrl = ScheduleController(ctrl.spots, new_fake_post)
        self.assertEqual(old_len, len(ctrl.spots))       # should merge that split spot back into one spot

    def test_bad_offsets(self):
        spots = spot_generate_dicts(60*60*3)
        new_fake_post = {
            ScheduleController.ACTION_KEY:'offset',
            ScheduleController.VALUES_KEY:{
                'index':1,
                'value':(60*60*3)*2
            }
        }
        self.assertRaises(BadSpotOffset, ScheduleController, spots, new_fake_post)

    def test_bad_index(self):
        spots = spot_generate_dicts(60*60*3)
        new_fake_post = {
            ScheduleController.ACTION_KEY:'delete',
            ScheduleController.VALUES_KEY:{
                'index':30000,
            }
        }
        self.assertRaises(IndexError, ScheduleController, spots, new_fake_post)


class ViewTests(TestCase):
    

    pass

