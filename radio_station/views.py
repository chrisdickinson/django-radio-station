from django.http import Http404
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext 
from django.db.models import Count
from radio_library.models import Artist
from models import Spot, Schedule, Show, DJ
import datetime
def create_r2r(func):
    def wrapped(request, *args, **kwargs):
        when = datetime.datetime.now()
        start_of_week = when - datetime.timedelta(days=when.weekday()) 
        context = func(request, *args, **kwargs)
        context.update({
            'week':[(start_of_week + datetime.timedelta(days=i)).date() for i in range(0, 7)],
            'now':when.date()
        })
        return render_to_response('radio_station/%s.html'%func.func_name, context, context_instance=RequestContext(request))
    return wrapped

def get_schedule_or_404(pk):
    try:
        if pk is None:
            return Schedule.objects.get_current_schedule()
        else:
            return Schedule.objects.get(pk=pk)
    except Schedule.DoesNotExist:
        raise Http404()

def schedule_weekday(request, day_of_week, schedule_pk=None):
    schedule = get_schedule_or_404(schedule_pk)
    try:
        weekday = int(day_of_week)
    except TypeError:
        weekday = datetime.datetime.now().weekday()
    except ValueError:
        weekday = 'MTWRFSU'.index(str(day_of_week))
    when = datetime.datetime.now()
    when = datetime.datetime(when.year, when.month, when.day, 0, 0)
    start_of_week = when - datetime.timedelta(days=when.weekday()) 
    when = start_of_week + datetime.timedelta(days=weekday)

    week = [start_of_week + datetime.timedelta(days=i) for i in range(0,7)]

    spots = Spot.objects.filter(schedule=schedule, day_of_week=weekday).order_by('day_of_week', 'offset', 'repeat_every')
    return {
        'weekday':when,
        'schedule':schedule,
        'spots':spots,
    }

def show_detail(request, show_slug, schedule_pk=None):
    schedule = get_schedule_or_404(schedule_pk)
    show = get_object_or_404(Show, slug=show_slug)
    favorite_artists = Artist.objects.filter(entry__show=show).annotate(playcount=Count('entry')).order_by('-playcount')[:5]
    spots = Spot.objects.filter(schedule=schedule, show=show)
    return {
        'show':show,
        'schedule':schedule,
        'favorite_artists':favorite_artists,
        'spots':spots,
    }

def dj_detail(request, dj_slug, schedule_pk=None):
    schedule = get_schedule_or_404(schedule_pk)
    dj = get_object_or_404(DJ, slug=dj_slug)
    favorite_artists = Artist.objects.filter(entry__dj=dj).annotate(playcount=Count('entry')).order_by('-playcount')[:5]
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
