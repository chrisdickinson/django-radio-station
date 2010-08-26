from django.db import models
from django.db.models import Q
from django.http import Http404
from radio.datetime import *
from radio.station.utils import *
import datetime
import itertools

class SpotManager(models.Manager):
    def __init__(self, schedule_class=None, *args, **kwargs):
        self.schedule_class = schedule_class
        return super(SpotManager, self).__init__(*args, **kwargs)

    def get_current_spot(self, when):
        """
            get_current_spot -> returns current Spot object if any, raises Spot.DoesNotExist if None
            takes `when` as a datetime object
        """
        schedule = self.schedule_class.objects.get_current_schedule(when)        
        repeat_options = self.model.REPEAT_CHOICES_DICT['Weekly'], get_nth_day_of_month(when)
        try:
            return self.filter(
                        schedule=schedule,
                        day_of_week=when.weekday(),
                        repeat_every__in=repeat_options,
                        offset__lte=get_offset_in_seconds(when)).order_by('-offset')[0]
        except IndexError:
            raise self.model.DoesNotExist

    def filter_next_spots_for_week(self, when):
        schedule = self.schedule_class.objects.get_current_schedule(when)
        repeat_options = self.model.REPEAT_CHOICES_DICT['Weekly'], get_nth_day_of_month(when)
        query = self.filter(schedule=schedule, repeat_every__in=repeat_options)

        weekday = when.weekday()

        lhs = Q(offset__gte=get_offset_in_seconds(when),
                day_of_week=weekday)
        rhs = Q(day_of_week__gt=weekday)
        query = query.filter(lhs | rhs)
        return query.order_by('day_of_week', 'offset')

    def next_spots(self, when):
        query = self.filter_next_spots_for_week(when)
        next_week = strip_hour_and_minute(datetime.timedelta(days=7-when.weekday()) + when)
        next_spots = self.filter_next_spots_for_week(next_week)
        query = ChainedQuerySet(query, next_spots)
        return query 

    def for_day(self, when):
        return self.filter(
            day_of_week__exact=when.weekday(),
            repeat_every__in=(self.model.REPEAT_CHOICES_DICT['Weekly'], get_nth_day_of_month(when))
        )

    def for_week(self, when):
        return self.filter(repeat_every__in=(self.model.REPEAT_CHOICES_DICT['Weekly'], get_nth_day_of_month(when)))
 
class ScheduleManager(models.Manager):
    def get_current_schedule(self, when):
        results = self.filter(start_date__lte=when, end_date__gte=when).order_by('-start_date')
        try:
            return results[0]
        except IndexError:
            raise self.model.DoesNotExist

    def get_current_schedule_or_404(self, when):
        try:
            return self.get_current_schedule(when)
        except self.model.DoesNotExist:
            raise Http404
