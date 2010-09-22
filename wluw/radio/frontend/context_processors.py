import datetime

def today(request):
    today = datetime.datetime.now()
    tomorrow = today+datetime.timedelta(days=1)
    day_after = tomorrow+datetime.timedelta(days=1)
    return {
        'today':today,
        'tomorrow':tomorrow,
        'day_after_tomorrow':day_after
    }
