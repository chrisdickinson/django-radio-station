from django import template
from tag_utils import define_parsed_tag
import datetime
register = template.Library()

def get_date(context, date, direction, num, units, target):
    direction_mul = { 
        'from':1,
        'before':-1
    }[str(direction)]
    num = num*direction_mul
    context.update({
        str(target):date+datetime.timedelta(days=num)
    })
    return u''

def get_date_range(context, from_date, until_date, target):
    delta = from_date - until_date
    context.update({
        str(target):(from_date+datetime.timedelta(days=i) for i in range(0, delta.days))
    })
    return u''

def alias(context, src, dst):
    context.update({
        str(dst):src,
    })
    return u''

define_parsed_tag(register, alias, "<src:any> to <dst:var>") 
define_parsed_tag(register, get_date, "<num:int> day(s) <direction:var> <date:any> as <target:var>") 
define_parsed_tag(register, get_date_range, "from <from_date:any> until <until_date:any> as <target:var>") 
