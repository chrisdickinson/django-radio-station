from django.template import RequestContext
from django.views.generic.date_based import object_detail, archive_day 
from django.shortcuts import render_to_response, get_object_or_404
from models import *
from utils import get_when_or_now
from composition import *

def event_detail_context(request, slug, year=None, month=None, day=None):
    when = get_when_or_now(year, month, day) 
    event = get_object_or_404(Event, date__exact=when, slug=slug)
    ctxt = {
        'event':event
    }
    return ctxt
event_detail = view_to_template('radio_events/event_detail.html')(event_detail_context)

def events_for_day_context(request, year=None, month=None, day=None):
    when = get_when_or_now(year, month, day).date()
    events = Event.objects.filter(date=when)
    ctxt = {
        'events':events,
        'day':when,
    }
    return ctxt
events_for_day = view_to_template('radio_events/event_list.html')(events_for_day_context)

def events_for_location_context(request, slug):
    location = get_object_or_404(Location, slug=slug)
    events = Event.objects.filter(location=location)
    ctxt = {
        'events':events,
        'location':location,
    }
    return ctxt
events_for_location = view_to_template('radio_events/event_list_location.html')(events_for_location_context)
