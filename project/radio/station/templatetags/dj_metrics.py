from tag_utils.nodes import *
from django import template
from wluw.station.models import *
from wluw.logs.models import *
from wluw.library.models import *
from django.db.models import Count

register = template.Library()

def get_dj_show(context, dj, *args, **kwargs):
    dj = statement(context, dj)
    now = datetime.datetime.now()
    try:
        show_schedule_relationship = ShowScheduleRelationship.objects.filter(dj=dj, schedule__start_date__lte=now, schedule__end_date__gte=now)[0]
        return show_schedule_relationship
    except IndexError:
        return None

def get_dj_top_tracks(context, dj, num=5, *args, **kwargs):
    dj = statement(context, dj)
    top_tracks = Track.objects.filter(entry__dj=dj).annotate(play_count=Count('entry')).order_by('-play_count')[0:int(num)]
    return top_tracks

def get_dj_top_artists(context, dj, num=5, *args, **kwargs):
    dj = statement(context, dj)
    top_artists = Artist.objects.filter(entry__dj=dj).annotate(play_count=Count('entry')).order_by('-play_count')[0:int(num)]
    return top_artists

SHOW_REGEX = "(?P<function>\w+) (?P<dj>[\w\.]+)"
METRICS_REGEX = "(?P<function>\w+)( (?P<num>\d+)?)? (?P<dj>[\w\.]+)"

register.tag('get_dj_show', generic_loader_tag(SHOW_REGEX, get_dj_show))
register.tag('get_dj_top_artists', generic_loader_tag(METRICS_REGEX, get_dj_top_artists))
register.tag('get_dj_top_tracks', generic_loader_tag(METRICS_REGEX, get_dj_top_tracks))

