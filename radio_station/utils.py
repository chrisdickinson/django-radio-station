import datetime
import itertools

def get_offset_in_seconds(time):
    start_of_day = datetime.datetime(time.year, time.month, time.day)
    return (time - start_of_day).seconds

def get_nth_day_of_month(time):
    return time.day / 7 + 1

class ChainedQuerySet(object):
    def __init__(self, *args):
        self.querysets = args

    def __getitem__(self, k):
        if not isinstance(k, (slice, int, long)):
            raise TypeError
        if isinstance(k, slice):
            offset_front = 0
            offset_end = 0
            if k.start is not None:
                offset_front = int(k.start)
            if k.stop is not None:
                offset_end = int(k.stop)

            current_off = offset_front
            current_left = offset_end
            qs_out = []
            for queryset in self.querysets:
                qs_len = len(queryset)
                if current_off < qs_len:
                    num = current_left - qs_len
                    if num >= 0:
                        qs_out.append(queryset[current_off:])
                        current_left -= num
                        current_off = 0
                    else:
                        qs_out.append(queryset[current_off:current_left])
                        break
            iterchain = itertools.chain(qs_out)
            output = []
            for qs in iterchain:
                for item in qs:
                    output.append(item)
            return output
        else:
            for queryset in self.querysets:
                qs_len = len(queryset)
                if k < qs_len:
                    return queryset[k]
                else:
                    k -= qs_len
        raise IndexError()
 
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
