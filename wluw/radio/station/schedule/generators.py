from radio.station.models import Schedule, Spot, Show, DJ
from exceptions import BadSpotIncrement
def spot_generate_dicts(increment, default_dj=None, default_show=None):
    if increment < 1:
        raise BadSpotIncrement('%d is an invalid spot increment' % increment)

    one_day = 60 * 60 * 24
    spots = []
    dj_pk = -1
    if default_dj:
       dj_pk = default_dj.pk
    show_pk = -1
    if default_show:
        show_pk = default_show.pk 

    for day in range(0, 7):
        for i in range(0, one_day, increment):
            spots.append({
                'day_of_week':day,
                'repeat_every':0,
                'offset':i,
                'dj_pk':dj_pk,
                'show_pk':show_pk,
                'pk':-1,
            })
    return spots

def spot_generate_objects(increment):
    pass

def spot_object_from_dict(dict):
    our_dict = {
        'day_of_week':dict['day_of_week'],
        'repeat_every':dict['repeat_every'],
        'offset':dict['offset'],
        'dj':DJ.objects.get(pk=dict['dj_pk']),
        'show':Show.objects.get(pk=dict['show_pk'])
    }
    return Spot(**our_dict)

def spot_dict_from_object(obj, overrides={}):
    spot_dict = {
        'day_of_week':obj.day_of_week,
        'repeat_every':obj.repeat_every,
        'offset':obj.offset,
        'dj_pk':obj.dj.pk,
        'show_pk':obj.show.pk,
        'pk':obj.pk,
    }
    spot_dict.update(overrides)
    return spot_dict

def spot_dicts_from_schedule(schedule, overrides={}):
    spots = Spot.objects.filter(schedule=schedule)
    spots_out = [spot_dict_from_object(spot, overrides) for spot in spots]
    return spots_out
