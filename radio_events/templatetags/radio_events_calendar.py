from django import template
from radio_events.models import Event
import datetime
import calendar
register = template.Library()

def calendar_block(today=None):
    if today is None:
        today = datetime.datetime.now()
    events = [event for event in Event.objects.filter(date__month=today.month, date__year=today.year)]
    calendar_month = calendar.monthcalendar(today.year, today.month)

    have_events = {}

    class Day(object):
        def __init__(self, day, has_event):
            self.day = day
            self.has_event = has_event
        def __unicode__(self):
            return "%d" % self.day
        def __eq__(self, rhs):
            return int(self.day) == int(rhs)
        def __ne__(self, rhs):
            return int(self.day) != int(rhs)

    weeks_out = []
    for week in calendar_month:
        week_out = []
        for day in week:
            has_event = False
            if day != 0:
                for event in events:
                    if event.date.day == day:
                        has_event = True
                        break
            week_out.append(Day(day, has_event))
        weeks_out.append(week_out)
    return {
        'calendar':weeks_out,
        'today':today
    }

calendar_block = register.inclusion_tag('radio_events/includes/calendar.html')(calendar_block)
