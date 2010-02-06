from django.contrib.auth.backends import ModelBackend
from .models import Schedule, DJ
import datetime 
class StationAuthBackend(ModelBackend):
    def authenticate(self, username=None, password=None):
        user = super(StationAuthBackend, self).authenticate(username, password)
        if user and not user.is_superuser:
            now = datetime.datetime.now()
            schedules = Schedule.objects.filter(start_date__lte=now, end_date__gte=now)
            dj = DJ.objects.filter(user=user, spot__schedule__in=schedules)
            if len(dj) < 1:
                return None
        return user
