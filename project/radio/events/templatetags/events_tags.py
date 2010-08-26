from django import template
from radio.events.models import Event
import datetime
import calendar
import itertools

register = template.Library()

def calendar_block_generator(today):
    events = Event.objects.filter(date__month=today.month, date__year=today.year)

    day_to_date = lambda x: datetime.date(today.year, today.month, x)
    event_on_day = lambda x: x != 0 and len([event for event in events if event.date == day_to_date(x)]) > 0
    calendar_month = calendar.monthcalendar(today.year, today.month)
    return (((day, event_on_day(day))        
        for day in week) 
        for week in calendar_month)

def calendar_block(today=None):
    if today is None:
        today = datetime.datetime.now()
    return {
            'today':today,
            'calendar':calendar_block_generator(today)
    }

calendar_block = register.inclusion_tag('events/includes/calendar.html')(calendar_block)
