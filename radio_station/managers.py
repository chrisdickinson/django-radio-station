from django.db import models
from django.db.models import Q
from utils import get_offset_in_seconds, get_nth_day_of_month, subscriptable_iterchain
import datetime
import itertools
class SpotManager(models.Manager):
    def __init__(self, *args, **kwargs):
        return super(SpotManager, self).__init__(*args, **kwargs)

    def get_current_spot(self, when=None):
        if when is None:
            when = datetime.datetime.now()

        from models import Schedule
        schedule = Schedule.objects.get_current_schedule()        
        kwargs = {
            'schedule':schedule,
            'day_of_week':when.weekday(),
            'repeat_every__in':(0, get_nth_day_of_month(when)),
            'offset__lte':get_offset_in_seconds(when),
        }
        return self.filter(**kwargs).order_by('-offset')[0]

    def filter_next_spots(self, when=None):
        if when is None:
            when = datetime.datetime.now()

        from models import Schedule
        schedule = Schedule.objects.get_current_schedule()
        base_filter = self.filter(schedule=schedule, repeat_every__in=(0, get_nth_day_of_month(when)))

        lhs_kwargs = {
            'offset__gte':get_offset_in_seconds(when),
            'day_of_week__exact':when.weekday(),
        }
        rhs_kwargs = {
            'day_of_week__gt':when.weekday(),
        }
        our_spots = base_filter.filter(Q(**lhs_kwargs) | Q(**rhs_kwargs)).order_by('day_of_week', 'offset') 
        if when.weekday() == 6:
            # this is a HACK
            tomorrow = when + datetime.timedelta(days=1)
            new_when = datetime.datetime(year=tomorrow.year, month=tomorrow.month, day=tomorrow.day, hour=0, minute=0)
            next_spots = self.filter_next_spots(new_when)
            our_spots = subscriptable_iterchain(our_spots, next_spots)
        return our_spots    


    def filter_schedule_for_day(self, when=None):
        if when is None:
            when = datetime.datetime.now()
        kwargs = {
            'day_of_week__exact':when.weekday(),
            'repeat_every__in':(0, get_nth_day_of_month(when)),
        }
        return self.filter(**kwargs)

    def filter_schedule_for_week(self, when=None):
        if when is None:
            when = datetime.datetime.now()
        kwargs = {
            'repeat_every__in':(0, get_nth_day_of_month(when)),
        }
        return self.filter(**kwargs)
 
class ScheduleManager(models.Manager):
    def get_current_schedule(self, when=None):
        if when is None:
            when = datetime.datetime.now()
        results = self.filter(start_date__lte=when, end_date__gte=when).order_by('-start_date')
        return results[0]

