import datetime

def get_when_or_now(*args):
    if None in args:
        return datetime.datetime.now()
    return datetime.datetime(*[int(arg) for arg in args])

