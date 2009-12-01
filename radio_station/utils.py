import datetime
import itertools

def get_nth_day_of_month(time):
    return time.day / 7 + 1

class ChainedQuerySet(object):
    def __init__(self, *args):
        self.querysets = args

    def __getitem__(self, k):
        if not isinstance(k, (slice, int, long)):
            raise TypeError
        if isinstance(k, slice):
            qs_out = []
            if k.stop is not None and k.stop < 0:
                raise IndexError()

            if k.step is None:
                k = slice(k.start, k.stop, 1)
            if k.start is None:
                k = slice(0, k.stop, k.step)

            def inner(k):
                for queryset in self.querysets:
                    result = queryset[k.start:k.stop:k.step]
                    for item in result:
                        yield item
                    if k.stop is not None:
                        len_result = len(result)
                        expected_len = (k.stop - k.start) / k.step
                        if expected_len > len_result:
                            left = (expected_len - len_result) * k.step
                            k = slice(0, left, k.step)
                        else:
                            raise StopIteration()
            output = inner(k)
            return [item for item in output] 
        else:
            if k < 0:
                raise IndexError()

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

def get_offset_in_seconds(dtime):
    start_of_day = strip_hour_and_minute(dtime)
    return (datetime.datetime(*dtime.timetuple()[:6]) - start_of_day).seconds
