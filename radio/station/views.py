from django.http import Http404
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext 
from django.db.models import Count
from radio.library.models import Artist
from radio.datetime import get_start_of_week, get_week_range, get_day_of_week
from .models import Spot, Schedule, Show, DJ
from composition import *
import datetime

def get_weekday_or_404(day_of_week):
    day_of_week = int(day_of_week)
    if day_of_week > 6 or day_of_week < 0:
        raise Http404
    return day_of_week

def schedule_for_day(request, schedule_pk, day_of_week):
    now = datetime.datetime.now()
    schedule = get_object_or_404(Schedule, pk=int(schedule_pk))
    weekday = get_weekday_or_404(day_of_week)
    spots = Spot.objects.filter(schedule=schedule, day_of_week=weekday).order_by('day_of_week', 'offset', 'repeat_every')
    template = 'station/for_day.html'
    context = {
        'weekday':weekday,
        'weekday_as_datetime':get_start_of_week(now)+datetime.timedelta(days=weekday),
        'schedule':schedule,
        'spots':spots,
        'week':get_week_range(now),
    }
    return render_to_response(template, context, context_instance=RequestContext(request))

def schedule_show_detail(request, schedule_pk, show_slug):
    now = datetime.datetime.now()
    schedule = get_object_or_404(Schedule, pk=int(schedule_pk))
    show = get_object_or_404(Show, slug=show_slug)
    spots = Spot.objects.filter(schedule=schedule, show=show)
    template = 'station/show_detail.html'
    context = {
        'show':show,
        'schedule':schedule,
        'spots':spots,
        'week':get_week_range(now),
    }
    return render_to_response(template, context, context_instance=RequestContext(request))

def schedule_dj_detail(request, dj_slug, schedule_pk=None):
    now = datetime.datetime.now()
    schedule = get_object_or_404(Schedule, pk=int(schedule_pk))
    dj = get_object_or_404(DJ, slug=dj_slug)
    spots = Spot.objects.filter(schedule=schedule, dj=dj)
    template = 'station/dj_detail.html'
    context = {
        'dj':dj,
        'schedule':schedule,
        'spots':spots,
        'week':get_week_range(now),
    }
    return render_to_response(template, context, context_instance=RequestContext(request))

def dj_detail(request, *args, **kwargs):
    now = datetime.datetime.now()
    schedule = Schedule.objects.get_current_schedule_or_404(now)
    return schedule_dj_detail(request, schedule_pk=schedule.pk, *args, **kwargs)

def show_detail(request, *args, **kwargs):
    now = datetime.datetime.now()
    schedule = Schedule.objects.get_current_schedule_or_404(now)
    return schedule_show_detail(request, schedule_pk=schedule.pk, *args, **kwargs)

def for_day(request, *args, **kwargs):
    now = datetime.datetime.now()
    schedule = Schedule.objects.get_current_schedule_or_404(now)
    return schedule_for_day(request, schedule_pk=schedule.pk, *args, **kwargs)
