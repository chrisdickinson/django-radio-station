# Create your views here.
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.db.models import Count
from django.http import Http404
from radio_library.models import Artist, Album 
from models import Entry 
from composition import *
import datetime
import itertools
import math

def time_to_ceiling(dtime, ceil):
    hour, minute = int(ceil) * int(math.ceil((dtime.hour+1)/float(ceil))), 0
    if hour > 23:
        hour,minute = 23, 59 
    return datetime.datetime(*(dtime.year,
                                dtime.month,
                                dtime.day,
                                hour,
                                minute))

def kwargs_to_time(*args):
    if None in args:
        return datetime.datetime.now()
    return datetime.datetime(*[int(arg) for arg in args])

def generate_nav_time(dtime, step, cap):
    off = datetime.datetime(dtime.year, dtime.month, dtime.day, 0, 0)
    while off < cap:
        yield off
        off += step

SPECIAL_NAMES = ( 
    'Midnight',
    '3a.m.',
    'Morning',
    '9a.m.',
    'Noon',
    '3p.m.',
    'Evening',
    '9p.m.',
    'Midnight',
)

def generate_date_radius(when, radius, cap, time=None):
    if time is None:
        time = (0, 0)
    td = datetime.timedelta
    days_until_cap = (cap.date() - when.date()).days
    if days_until_cap > radius:
        days_until_cap = radius
    to_flat_date = lambda x: datetime.datetime(x.year, x.month, x.day, *time)
    end_date = to_flat_date(when) + td(days=days_until_cap)

    day = radius*2
    while day > -1:
        yield end_date-td(days=day)
        day -= 1 

def date_radius(when, radius, cap, time=None):
    return [i for i in generate_date_radius(when, radius, cap, time)]

def time_context(request, year=None, month=None, day=None, hour=None, min=0):
    now = datetime.datetime.now()
    now_ceil = time_to_ceiling(now, 3.0)
    three_hours = datetime.timedelta(seconds=60*60*3)

    when = kwargs_to_time(year, month, day, hour, min)
    when_ceil = time_to_ceiling(when, 3.0) 

    if when_ceil > now_ceil:
        raise Http404()

    prev_time, next_time = when_ceil - three_hours - three_hours, when_ceil + three_hours
    cap = datetime.datetime(when.year, when.month, when.day, 23, 59)
    if now.date() == when.date():
        cap = datetime.datetime(cap.year, cap.month, cap.day, now_ceil.hour, now_ceil.minute)

    nav_time_range = generate_nav_time(when, three_hours, cap)
    nav_time_range = itertools.izip(SPECIAL_NAMES, nav_time_range)
    nav_date_range = generate_date_radius(when, 3, now)

    logs = Entry.objects.filter(submitted__lte=when_ceil, submitted__gt=prev_time).order_by('-submitted')
    ctxt = {
        'logs':logs,
        'when':when,
        'now':now,
        'time_range':nav_time_range,
        'date_range':nav_date_range,
        'prev_time':prev_time,
        'next_time':next_time,
    }
    return ctxt
time_view = view_to_template('radio_logs/logs_time.html')(time_context)

def chart_view(request, year=None, month=None, week=None, what=None, rotation=False):
    if what is None:
        what = 'artist'
    if None in (year, month, week):
        when = datetime.datetime.now()
        year = when.year
        month = when.month
        week = when.day/7+1
    week = int(week)
    if week < 0 or week > 6:
        raise Http404()

    month_start = datetime.datetime(*[int(i) for i in (year, month, 1)])
    month_start = month_start - datetime.timedelta(days=month_start.weekday())
    start_week = month_start + datetime.timedelta(days=7*week)
    end_week = start_week + datetime.timedelta(days=7)

    prev_week = start_week - datetime.timedelta(days=1)
    prev_week_no = prev_week.day/7+1 

    next_week = end_week+datetime.timedelta(days=1)
    next_week_no = next_week.day/7+1

    what_model = None
    prefix = u''
    try:
        if what is None:
            what = 'album'

        what_model = {'artist':Artist, 'album':Album}[str(what)]
        prefix = {'artist':'', 'album':'artist__'}[str(what)]
    except IndexError:
        raise Http404()

    submitted_kwargs = {
        '%sentry__submitted__lt'%prefix:end_week,
        '%sentry__submitted__gte'%prefix:start_week,
    }
    annotate_kwargs = {
        'playcount':Count('%sentry'%prefix),
    }

    items = what_model.objects.filter(**submitted_kwargs).annotate(**annotate_kwargs).order_by('-playcount')

    if rotation:
        is_rotation_kwargs = {
            '%sentry__is_rotation'%prefix:True,
        }
        items = items.filter(**is_rotation_kwargs)

    if what_model is Album:
        items = [{
            'name':'%s - %s' % (album.artist.name, album.name),
            'playcount':album.playcount
        } for album in items]
    else:
        items = [{
            'name':artist.name,
            'playcount':artist.playcount
        } for artist in items]

    ctxt = {
        'items':items[:30],
        'week':start_week,
        'week_no':start_week.day/7+1,
        'prev_week':prev_week,
        'prev_week_no':prev_week_no,
        'next_week':next_week,
        'next_week_no':next_week_no,
    }
    return render_to_response('radio_logs/charts_view.html', ctxt, context_instance=RequestContext(request))
