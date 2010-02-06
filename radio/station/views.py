from django.http import Http404
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext 
from django.db.models import Count
from radio.library.models import Artist
from .utils import get_start_of_week, get_week_range, get_day_of_week
from .models import Spot, Schedule, Show, DJ
from composition import *
import datetime

def get_schedule_or_404(pk):
    try:
        if pk is None:
            return Schedule.objects.get_current_schedule()
        else:
            return Schedule.objects.get(pk=pk)
    except Schedule.DoesNotExist:
        raise Http404()

def week_range_context(request, *args, **kwargs):
    now = datetime.datetime.now()
    return {
        'week':get_week_range(now),
        'now':now.date()
    }

def schedule_weekday_context(request, day_of_week, schedule_pk=None):
    schedule = get_schedule_or_404(schedule_pk)
    try:
        weekday = int(day_of_week)
    except TypeError:
        weekday = datetime.datetime.now().weekday()
    except ValueError:
        weekday = 'MTWRFSU'.index(str(day_of_week))
    weekday = get_day_of_week(weekday)
    spots = Spot.objects.filter(schedule=schedule, day_of_week=weekday.weekday()).order_by('day_of_week', 'offset', 'repeat_every')
    return {
        'weekday':weekday,
        'schedule':schedule,
        'spots':spots,
    }

def show_detail_context(request, show_slug, schedule_pk=None):
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

def dj_detail_context(request, dj_slug, schedule_pk=None):
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

schedule_weekday = view_to_template('radio.station/schedule_weekday.html')(
    compose_response(
        schedule_weekday_context,
        week_range_context,
    )
)
show_detail = view_to_template('radio.station/show_detail.html')(
        compose_response(
            show_detail_context,
            week_range_context,
        )
)
dj_detail = view_to_template('radio.station/dj_detail.html')(
    compose_response(
        dj_detail_context,
        week_range_context,
    )
)
