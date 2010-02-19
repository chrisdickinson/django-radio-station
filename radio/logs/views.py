# Create your views here.
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.db.models import Count
from django.http import Http404
from radio.events.utils import get_when_or_now
from radio.library.models import Artist, Album 
from radio.datetime import *
from models import Entry 
from composition import *
import datetime

def time_view(request, year=None, month=None, day=None, hour=0, min=0):
    parsed_month = None if month is None else datetime.datetime.strptime(month, '%b').month
    at_datetime = get_when_or_now(year, parsed_month, day, hour, min)
    current_datetime = datetime.datetime.now()

    radius_in_seconds = 60 * 60 * 3     # 3 hours
    at_datetime_offset = get_offset_in_seconds(at_datetime)
    start_of_day = strip_hour_and_minute(at_datetime)

    at_datetime = start_of_day + datetime.timedelta(seconds=radius_in_seconds*(at_datetime_offset/radius_in_seconds))

    if at_datetime > current_datetime:
        raise Http404

    end_datetime = at_datetime + datetime.timedelta(seconds=radius_in_seconds)
    entries = Entry.objects.filter(submitted__lte=end_datetime, submitted__gte=at_datetime)

    context = {
        'entries':entries,
        'prev':at_datetime-datetime.timedelta(seconds=radius_in_seconds),
        'next':end_datetime if end_datetime < current_datetime else None,
        'current_datetime':current_datetime,
        'at_datetime':at_datetime,
        'end_datetime':end_datetime,
        'date_range':(dt for dt in generate_datetime_radius(at_datetime, 3) if dt <= current_datetime),
        'time_range':(datetime.timedelta(seconds=x*60*60)+start_of_day
                    for x in range(0,24,3) 
                    if (datetime.timedelta(seconds=x*60*60)+start_of_day) <= current_datetime)
    }
    return render_to_response('logs/logs_time.html', context, context_instance=RequestContext(request))

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
    return render_to_response('radio.logs/charts_view.html', ctxt, context_instance=RequestContext(request))
