from django.db import models
from django.contrib.auth.models import User
from managers import SpotManager, ScheduleManager

class Spot(models.Model):
    objects = SpotManager()
    DAY_CHOICES = (
        (0, 'Monday'),
        (1, 'Tuesday'),
        (2, 'Wednesday'),
        (3, 'Thursday'),
        (4, 'Friday'),
        (5, 'Saturday'),
        (6, 'Sunday'),
    )
    REPEAT_CHOICES = (
        (0, 'Weekly'),
        (1, '1st day of month'),
        (2, '2nd day of month'),
        (3, '3rd day of month'),
        (4, '4th day of month'),
        (5, '5th day of month'),
        (6, '6th day of month'),
        (7, 'Never'),
    )
    day_of_week = models.IntegerField(choices=DAY_CHOICES)
    repeat_every = models.IntegerField(choices=REPEAT_CHOICES)
    offset = models.PositiveIntegerField()                  #offset from 12:00AM in seconds
    dj = models.ForeignKey('DJ')
    show = models.ForeignKey('Show')
    schedule = models.ForeignKey('Schedule')

class Show(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    special_program = models.BooleanField()
    active = models.BooleanField()
    date_added = models.DateTimeField()
    image = models.ImageField(upload_to="usr/shows")
    blurb = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    schedule = models.ManyToManyField("Schedule", through=Spot)

    def __unicode__(self): 
        return "%s" % self.name

    def get_spots(self, schedule=None):
        try:
            if schedule is None:
                schedule = Schedule.objects.get_current_schedule()
            return Spot.objects.filter(schedule=schedule, show=self)
        except Schedule.DoesNotExist, e:
            return None
        except Schedule.MultipleObjectsReturned, e:
            return None 

class Schedule(models.Model):
    objects = ScheduleManager()
    start_date = models.DateField()
    end_date = models.DateField()

class DJ(models.Model):
    account = models.OneToOneField(User)
    slug = models.SlugField(unique=True)
    summary = models.TextField()
    description = models.TextField()
