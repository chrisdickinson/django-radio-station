from django import template
from wluw.station.models import *
from tag_utils.nodes import *

import datetime
register = template.Library()

def seconds_to_time(value):
    value = int(value)
    hour = value / 3600
    minute = (value % 3600) / 60
    time = datetime.time(hour, minute)
    return time

def day_of_week_to_time(value):
    now = datetime.datetime.now()
    weekday = now.weekday()
    delta = datetime.timedelta(days=weekday-value) 
    return now - delta

GET_SHOW_RELATIONSHIP_FOR = "(?P<function>\w+) (?P<show>[\w\.]+) (?P<schedule>[\w\.]+)"
def get_show_relationship_for(context, show, schedule, *args, **kwargs):
    show = statement(context, show)
    schedule = statement(context, schedule)
    return show.get_relationship_for(schedule)

GET_OTHER_SHOW_RELATIONSHIPS = "(?P<function>\w+) (?P<show>[\w\.]+) (?P<schedule>[\w\.]+)"
def get_other_show_relationships(context, show, schedule, *args, **kwargs):
    show = statement(context, show)
    schedule = statement(context, schedule)
    return show.get_all_past_relationships(schedule)

current_show_get = loader_tag(ShowScheduleRelationship, defaults={'method':'get_current_show_relationship'}, limit_func=SINGLE_VALUE)
next_schedule_get = loader_tag(ShowScheduleRelationship, defaults={'method':'get_next_show_relationships'})
register.filter('seconds_to_time', seconds_to_time)
register.filter('day_of_week_to_time', day_of_week_to_time)
register.tag('next_schedule_get', next_schedule_get)
register.tag('get_current_show', current_show_get)
register.tag('get_show_relationship_for', generic_loader_tag(GET_SHOW_RELATIONSHIP_FOR, get_show_relationship_for))
register.tag('get_other_show_relationships', generic_loader_tag(GET_OTHER_SHOW_RELATIONSHIPS, get_other_show_relationships))

