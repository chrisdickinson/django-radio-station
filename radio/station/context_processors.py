from django.conf import settings
import datetime

def current_datetime(request):
    return {
        'current_datetime':datetime.datetime.now()
    }

def google_analytics(request):
    return {
        'GOOGLE_ANALYTICS_ACCOUNT':getattr(settings, 'GOOGLE_ANALYTICS_ACCOUNT', None),
    }
