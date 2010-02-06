from exceptions import UnsupportedAction, BadSpotOffset
from django.utils import simplejson
from django.utils.safestring import mark_safe

class ScheduleController(object):
    ACTION_KEY = 'edit'
    VALUES_KEY = 'values'
    def action_is_okay(self, action):
        return action.is_public

    def __init__(self, spots, post):
        self.spots = spots
        self.post = post
        if ScheduleController.ACTION_KEY in self.post.keys():
            action = getattr(self, self.post[ScheduleController.ACTION_KEY])
            if self.action_is_okay(action):
                self.spots = action(**self.post[ScheduleController.VALUES_KEY])
            else:
                raise UnsupportedAction('%s is an unsupported action.' % self.post[ScheduleController.ACTION_KEY]) 

    def get_next_spot(self, spot):
        spots_that_day = [s for s in self.spots if s['day_of_week']==spot['day_of_week'] and s['offset'] != spot['offset']]
        closest_spot_distance = 60*60*24
        next_spot = None 
        for s in spots_that_day:
            dist = s['offset'] - spot['offset']
            if dist > 0 and dist < closest_spot_distance:
                closest_spot_distance = dist
                next_spot = s
        if next_spot is None:
            next_spot = {
                'offset':60*60*24
            }
        return next_spot

    def get_previous_spot(self, spot):
        spots_that_day = [s for s in self.spots if s['day_of_week']==spot['day_of_week'] and s['offset'] != spot['offset']]
        closest_spot_distance = 60*60*24
        next_spot = None 
        for s in spots_that_day:
            dist = spot['offset'] - s['offset']
            if dist > 0 and dist < closest_spot_distance:
                closest_spot_distance = dist
                next_spot = s
        if next_spot is None:
            next_spot = {
                'offset':-1
            }
        return next_spot

    def get_associated_spots(self, spot):
        if spot['repeat_every'] == 0:
            return [spot]
        spots = [spot]
        for _spot in self.spots:
            if _spot['offset'] == spot['offset'] and _spot['day_of_week'] == spot['day_of_week']:
                spots.append(_spot)
        return spots

    def repeat_every(self, index, value):
        spot = self.spots[index]
        spots = [] + self.spots 
        if spot['repeat_every'] == 0 and value != 0:
            spot['repeat_every'] = value
            # we've gotta split this across weeks.
            for i in range(0, 6):
                if i+1 == value:
                    continue
                new_spot = {}
                new_spot.update(spot)
                new_spot['repeat_every'] = i+1
                spots.append(new_spot)
        elif spot['repeat_every'] != 0 and value == 0:
            _spots = self.get_associated_spots(spot)
            for s in _spots:
                if s == spot:
                    continue
                spots.remove(s)
            spot['repeat_every'] = 0 
        return spots
    repeat_every.is_public = True

    def delete(self, index):
        spot = self.spots[index]
        self.spots.remove(spot)
        return self.spots
    delete.is_public = True

    def add(self, index, value):
        return self.spots
    add.is_public = True

    def offset(self, index, value):
        spot = self.spots[index]
        previous_spot = self.get_previous_spot(spot)
        next_spot = self.get_next_spot(spot)
        if value < 0 or value <= previous_spot['offset'] or value >= next_spot['offset']:
            raise BadSpotOffset('%d is a bad spot offset -- interferes with next or previous spot' % value)

        associated_spots = self.get_associated_spots(spot)
        for _spot in associated_spots:
            _spot['offset'] = value
        return self.spots
    offset.is_public = True

    def spots_to_json(self):
        return mark_safe(simplejson.dumps(self.spots))
