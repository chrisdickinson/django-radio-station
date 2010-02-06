from django import forms
from radio.station.models import DJ, Show, Schedule
def hour_choices():
    return [(seconds, '%d hours' % (seconds/3600)) for seconds in range(3600, 90000, 3600)]
HOUR_CHOICES = hour_choices()

def queryset_iterable(qs, blank=None):
    if blank:
        yield ('', '---')
    qs = qs()
    for q in qs:
        yield (q.pk, str(q))

class GenerateScheduleForm(forms.Form):
    increment = forms.ChoiceField(choices=HOUR_CHOICES)
    default_dj = forms.ChoiceField(choices=queryset_iterable(DJ.objects.all, True), required=False)
    default_show = forms.ChoiceField(choices=queryset_iterable(Show.objects.all, True), required=False)

class CopyScheduleForm(forms.Form):
    schedule = forms.ChoiceField(choices=queryset_iterable(Schedule.objects.all, True))

