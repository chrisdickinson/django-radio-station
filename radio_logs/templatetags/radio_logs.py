from django import template
from ..models import Entry
from tag_utils import define_parsed_node 
import datetime
register = template.Library()

def playlist_table(when=None, how_many=15):
    if when is None:
        when = datetime.datetime.now()
    objects = Entry.objects.all().order_by('-submitted')
    return {
        'logs':objects
    }

def grab_latest_logs(context, target, number=None):
    if number is None:
        number = 30
    now = datetime.datetime.now()
    logs = Entry.objects.filter(submitted__lte=now).order_by('-submitted')[:number]
    context.update({
        str(target):logs,
    })
    return u''

define_parsed_node(register, grab_latest_logs, "(get <number:int> )as <target:var>")
playlist_table = register.inclusion_tag('radio_logs/includes/playlist.html')(playlist_table)
