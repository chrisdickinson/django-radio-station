from django.template import RequestContext
from django.views.generic.date_based import object_detail, archive_day 
from django.shortcuts import render_to_response, get_object_or_404
from models import *
from utils import get_when_or_now
from radio.datetime import generate_datetime_radius 
from composition import *
import datetime

def event_detail_context(request, slug, year=None, month=None, day=None):
    when = get_when_or_now(year, month, day) 
    event = get_object_or_404(Event, date__exact=when, slug=slug)
    ctxt = {
        'when':when,
        'event':event,
        'week':generate_datetime_radius(when, 3) 
    }
    return ctxt
event_detail = view_to_template('events/event_detail.html')(event_detail_context)

def events_for_day_context(request, year=None, month=None, day=None):
    when = get_when_or_now(year, month, day)
    events = Event.objects.filter(date=when)
    ctxt = {
        'when':when,
        'events':events,
        'day':when,
        'week':generate_datetime_radius(when, 3) 
    }
    return ctxt
events_for_day = view_to_template('events/event_list.html')(events_for_day_context)

def events_for_location_context(request, slug):
    when = datetime.datetime.now()
    location = get_object_or_404(Location, slug=slug)
    events = Event.objects.filter(location=location)
    ctxt = {
        'when':when,
        'events':events,
        'location':location,
        'week':generate_datetime_radius(when, 3) 
    }
    return ctxt
events_for_location = view_to_template('events/event_list_location.html')(events_for_location_context)
