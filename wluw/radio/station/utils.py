import datetime
import itertools

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
