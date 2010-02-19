import datetime
import itertools
import math

def datetime_to_ceiling(dtime, ceil):
    hour, minute = int(ceil) * int(math.ceil((dtime.hour+1)/float(ceil))), 0
    if hour > 23:
        hour, minute = 23, 59 
    return datetime.datetime(*(dtime.year,
                                dtime.month,
                                dtime.day,
                                hour,
                                minute))

def generate_datetime_radius(center, radius, time=(0, 0)):
    to_flat_date = lambda x: datetime.datetime(x.year, x.month, x.day, *time)
    end_date = to_flat_date(center) + datetime.timedelta(days=radius)

    circumference = radius*2
    return [(end_date-datetime.timedelta(days=day)) for day in range(circumference, -1, -1)]

def cap_date_radius(date_radius, cap_date, operation='__lt__'):
    cmp = getattr(cap_date, operation)
    return (dt for dt in datetime_radius if cmp(dt.date())) 
 
def get_nth_day_of_month(time):
    return time.day / 7 + 1

def get_start_of_week(dtime=None):
    if dtime is None:
        dtime = datetime.datetime.now()
    start_of_week = dtime.date() - datetime.timedelta(days=dtime.weekday())
    return datetime.datetime(start_of_week.year, start_of_week.month, start_of_week.day, 0, 0)

def get_week_range(dtime=None):
    if dtime is None:
        dtime = datetime.datetime.now()
    start_of_week = get_start_of_week(dtime)
    return ((start_of_week + datetime.timedelta(days=i)).date() for i in range(0, 7))

def get_day_of_week(day, dtime=None):
    if dtime is None:
        dtime = datetime.datetime.now()
    start_of_week = get_start_of_week(dtime)
    return start_of_week + datetime.timedelta(days=day) 

def strip_hour_and_minute(dtime):
    return datetime.datetime(*[i for i in itertools.chain(dtime.timetuple()[:3], (0, 0))])

def get_offset_in_seconds(dtime):
    start_of_day = strip_hour_and_minute(dtime)
    return (datetime.datetime(*dtime.timetuple()[:6]) - start_of_day).seconds

def get_when_or_now(*args):
    if None in args:
        return datetime.datetime.now()
    return datetime.datetime(*[int(arg) for arg in args])

