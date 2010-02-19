from django import template
from tag_utils import define_parsed_tag
from radio.frontend.models import Ad
import datetime
import random
register = template.Library()

def get_random_ad(context, asvar):
    now = datetime.datetime.now()
    ads = Ad.objects.filter(start_date__lte=now, end_date__gte=now)
    num_ads = len(ads)
    rand_index = int(random.random() * num_ads)
    if num_ads:
        context[str(asvar)] = ads[rand_index]
    return u''

define_parsed_tag(register, get_random_ad, 'as <asvar:var>')
