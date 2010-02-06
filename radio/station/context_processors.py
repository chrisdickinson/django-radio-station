from django.conf import settings

def google_analytics(request):
    return {
        'GOOGLE_ANALYTICS_ACCOUNT':getattr(settings, 'GOOGLE_ANALYTICS_ACCOUNT', None),
    }
