from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.flatpages.models import FlatPage
from radio.staff.models import StaffRoleRelation
from django.db.models import Q
from radio.station.models import Spot, Schedule
from radio.events.models import Event
from radio.logs.models import Entry
from django.template import loader, RequestContext
from django import http

def server_error(request, template_name='500.html'):
    t = loader.get_template(template_name) # You need to create a 500.html template.
    return http.HttpResponseServerError(t.render(RequestContext(request, {})))

def home(request):
    import datetime
    now = datetime.datetime.now()

    schedule = Schedule.objects.get_current_schedule(now)
    current_spot = Spot.objects.get_current_spot(now)
    next_spots = Spot.objects.next_spots(now)[:6]
    weekday_str = 'MTWRFSU'[current_spot.to_datetime.weekday()]
    latest_logs = Entry.objects.all().order_by('-submitted')[0:10]

    today = datetime.datetime.now()
    tomorrow = today+datetime.timedelta(days=1)
    day_after = tomorrow+datetime.timedelta(days=1)

    roles = StaffRoleRelation.objects.filter(Q(schedule__pk=schedule.pk)|Q(schedule__pk__isnull=True))
    about_page = FlatPage.objects.get(url='/about/')

    events = {
        'today':Event.objects.filter(date=today).order_by('-weight')[:3],
        'tomorrow':Event.objects.filter(date=tomorrow).order_by('-weight')[:3],
        'day_after':Event.objects.filter(date=day_after).order_by('-weight')[:3],
    }

    start_of_week = now - datetime.timedelta(days=now.weekday()) 

    ctxt = {
        'current_spot':current_spot,
        'next_spots':next_spots,
        'weekday_str':weekday_str,
        'events':events,
        'schedule':schedule,
        'logs':latest_logs,
        'about_page':about_page,
        'week':[(start_of_week + datetime.timedelta(days=i)).date() for i in range(0, 7)],
        'now':now.date(),
        'roles':roles,
    }
    return render_to_response('home.html', ctxt, context_instance=RequestContext(request)) 
