from django.template import RequestContext
from django.views.generic.date_based import object_detail, archive_day 
from django.shortcuts import render_to_response, get_object_or_404
from models import *
import datetime

def get_when_or_now(year, month, day):
    when = datetime.datetime.now()
    if None not in (year, month, day):
        when = datetime.datetime(*[int(i) for i in year, month, day])
    return when 

def event_detail(request, slug, year=None, month=None, day=None):
    when = get_when_or_now(year, month, day) 
    event = get_object_or_404(Event, date__exact=when, slug=slug)
    ctxt = {
        'event':event
    }
    return render_to_response('radio_events/event_detail.html', ctxt, context_instance=RequestContext(request))

def events_for_day(request, year=None, month=None, day=None):
    when = get_when_or_now(year, month, day).date()
    events = Event.objects.filter(date=when)
    ctxt = {
        'events':events,
        'day':when,
    }
    return render_to_response('radio_events/event_list.html', ctxt, context_instance=RequestContext(request))

def events_for_location(request, slug):
    location = get_object_or_404(Location, slug=slug)
    events = Event.objects.filter(location=location)
    ctxt = {
        'events':events,
        'location':location,
    }
    return render_to_response('radio_events/event_list_location.html', ctxt, context_instance=RequestContext(request))
