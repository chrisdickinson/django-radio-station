import datetime
import itertools

def get_offset_in_seconds(time):
    start_of_day = datetime.datetime(time.year, time.month, time.day)
    return (time - start_of_day).seconds

def get_nth_day_of_month(time):
    return time.day / 7 + 1

class subscriptable_iterchain(object):
    """
        hacky way to chain querysets together and still allow that lovely
        slice-limiting we've all come to know and love.
    """
    def __init__(self, *args):
        self.iterchain = itertools.chain(*args)

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
            index = 0
            while index < offset_front:
                self.iterchain.next()
            output = []
            for i in range(0, offset_end):
                output.append(self.iterchain.next())
            return output
