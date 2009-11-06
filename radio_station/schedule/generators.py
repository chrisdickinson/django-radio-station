from radio_station.models import Schedule, Spot, Show, DJ
from exceptions import BadSpotIncrement
def spot_generate_dicts(increment):
    if increment < 1:
        raise BadSpotIncrement('%d is an invalid spot increment' % increment)

    one_day = 60 * 60 * 24
    spots = []
    for day in range(0, 7):
        for i in range(0, one_day, increment):
            spots.append({
                'day_of_week':day,
                'repeat_every':0,
                'offset':i,
                'dj_pk':-1,
                'show_pk':-1,
            })
    return spots

def spot_generate_objects(increment):
    pass

def spot_object_from_dict(dict):
    our_dict = {
        'day_of_week':dict['day_of_week'],
        'repeat_every':dict['repeat_every'],
        'offset':dict['offset'],
        'dj':DJ.objects.get(dict['dj_pk']),
        'show':Show.objects.get(dict['show_pk'])
    }
    return Spot(**our_dict)

def spot_dict_from_object(object):
    pass
