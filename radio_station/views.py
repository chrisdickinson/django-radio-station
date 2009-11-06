from django.http import Http404
from django.shortcuts import render_to_response, get_object_or_404
from django.template import request_context
from django.db.models import Count
from radio_library.models import Artist
from models import Spot, Schedule, Show, DJ
def create_r2r(func):
    def wrapped(request, *args, **kwargs):
        return render_to_response('radio_station/%s.html'%func.func_name, func(request, *args, **kwargs), context_instance=RequestContext(request))
    return wrapped

def schedule_or_404(pk):
    try:
        if pk is None:
            return Schedule.objects.get_current_schedule()
        else:
            return Schedule.objects.get(pk=pk)
    except Schedule.DoesNotExist:
        raise Http404()

def schedule_weekday(request, day_of_week, schedule_pk=None):
    schedule = get_schedule_or_404(schedule_pk)
    weekday = 'MTWRFSU'.index(str(day_of_week))
    spots = Spot.objects.filter(schedule=schedule, day_of_week=weekday).order_by('day_of_week', 'offset', 'repeat_every')
    return {
        'weekday':weekday,
        'schedule':schedule,
        'spots':spots,
    }

def show_detail(request, show_slug, schedule_pk=None):
    schedule = get_schedule_or_404(schedule_pk)
    show = get_object_or_404(Show, spot_set__schedule=schedule, slug=show_slug)
    favorite_artists = Artist.object.filter(entry__show=show).annotate(playcount=Count('entry')).order_by('-playcount')[:5]
    spots = Spot.objects.filter(schedule=schedule, show=show)
    return {
        'show':show,
        'schedule':schedule,
        'favorite_artists':favorite_artists,
        'spots':spots,
    }

def dj_detail(request, dj_slug, schedule_pk=None):
    schedule = get_schedule_or_404(schedule_pk)
    dj = get_object_or_404(dj, spot_set__schedule=schedule, slug=dj_slug)
    favorite_artists = Artist.object.filter(entry__dj=dj).annotate(playcount=Count('entry')).order_by('-playcount')[:5]
    spots = Spot.objects.filter(schedule=schedule, dj=dj)
    return {
        'dj':dj,
        'schedule':schedule,
        'favorite_artists':favorite_artists,
        'spots':spots,
    }

dj_detail = create_r2r(dj_detail)
show_detail = create_r2r(show_detail)
schedule_weekday = create_r2r(schedule_weekday) 
