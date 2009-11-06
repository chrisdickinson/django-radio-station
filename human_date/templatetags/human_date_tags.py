from tag_utils import define_parsed_tag
from django import template
import datetime

register = template.Library()

def human_relative_date(context, date):
    now = datetime.datetime.now()
    diff = now - date
    is_past = diff.seconds > 0
    diff_seconds = abs(diff.seconds)

    time_string = ''
    if diff_seconds < 60:
        time_string = 'a few moments'
    elif diff_seconds < 60*10:
        time_string = 'a few minutes'
    elif diff_seconds < 3600:
        time_string = '%d minutes' % (diff_seconds/60)
    else:
        if time_string > 3600 and time_string <= 7200:
            time_string = 'an hour'
        elif time_string < 3600*3:
            time_string = 'a few hours'
        else:
            time_string = '%d hours' % (diff_seconds/3600)

    if is_past:
        time_string = '%s ago' % time_string
    else:
        time_string = 'in %s' % time_string
    return time_string

define_parsed_tag(register, human_relative_date, '<date:any>')
