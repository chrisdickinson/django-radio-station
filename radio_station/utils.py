import datetime

def get_offset_in_seconds(time):
    start_of_day = datetime.datetime(time.year, time.month, time.day)
    return (time - start_of_day).seconds

def get_nth_day_of_month(time):
    return time.day / 7 + 1

