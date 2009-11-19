# Create your views here.
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.db.models import Count
from django.http import Http404
from radio_library.models import Artist, Album 
from models import Entry 
import datetime
import math

def time_view(request, year=None, month=None, day=None, hour=None):
    when = None
    now = datetime.datetime.now()
    now = datetime.datetime(now.year, now.month, now.day, int(3 * math.ceil(now.hour/3.0)), 0)
    if None in (year, month, day, hour):
        when = datetime.datetime(now.year, now.month, now.day, now.hour, 0)
    else:
        when = datetime.datetime(*[int(i) for i in year, month, day, hour, 0])
    three_hours = datetime.timedelta(seconds=60*60*3)
    prev_time = when - three_hours 
    next_time = when + three_hours
    logs = Entry.objects.filter(submitted__lte=when, submitted__gt=prev_time).order_by('-submitted')

    if next_time > now:
        next_time = None
    time_range_start = datetime.datetime(when.year, when.month, when.day, 0, 0)
    time_range = []
    special_names = {
        0:'Midnight',
        3:'3a.m.',
        6:'Morning',
        9:'9a.m.',
        12:'Noon',
        15:'3p.m.',
        18:'Evening',
        21:'9p.m.',
    }
    for i in range(0, 24, 3):
        offset = time_range_start + datetime.timedelta(seconds=i*60*60)
        if offset <= when:
            name = special_names[i]
            time_range.append({
                'name':name,
                'time':offset,
            })

    date_range = []
    start_date_range = 3 
    for i in range(-start_date_range, start_date_range):
        offset = when + datetime.timedelta(days=i)
        if offset.date() <= now.date():
            date_range.append(datetime.datetime(offset.year, offset.month, offset.day, offset.hour, 0))

    ctxt = {
        'logs':logs,
        'time':when,
        'time_range':time_range,
        'date_range':date_range,
        'today':now,
        'next_time':next_time,
        'prev_time':prev_time,
    }
    return render_to_response('radio_logs/logs_time.html', ctxt, context_instance=RequestContext(request))

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
