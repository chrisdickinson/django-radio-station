from tag_utils import define_parsed_tag 
from radio.logs.models import Entry
from django import template
import datetime
register = template.Library()

def playlist_table(when=None, how_many=5):
    if when is None:
        when = datetime.datetime.now()
    objects = Entry.objects.all().order_by('-submitted')[:int(how_many)]
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

define_parsed_tag(register, grab_latest_logs, "(get <number:int> )as <target:var>")
playlist_table = register.inclusion_tag('logs/includes/playlist.html')(playlist_table)
