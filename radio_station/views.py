from django.views.generic.list_detail import object_list, object_detail
from django.http import Http404
from models import Schedule, Show, Spot, DJ
from django.shortcuts import render_to_response
from django.template import RequestContext
import datetime

def schedule_list(request, page):
    now = datetime.datetime.now()
    schedules = Schedule.objects.filter(start_date__lte=now)
    ctxt = {
        'schedule_list':schedules,
    }
    return render_to_response('radio_station/schedule_list.html', ctxt, context_instance=RequestContext(request))

def schedule_metrics(request, schedule_pk):
    return None

def schedule_spot_list(request, schedule_pk=None):
    schedule = None
    try:
        if schedule_pk is None:
            schedule = Schedule.objects.get_current_schedule()
        else:
            schedule = Schedule.objects.get(pk=schedule_pk)
    except:
        raise Http404()

    spots = Spot.objects.filter(schedule__pk=schedule_pk).order_by('day_of_week', 'offset', 'repeat_every')
    ctxt = {
        'spots':spots,
    }
    return render_to_response('radio_station/schedule_list_spots.html', ctxt, context_instance=RequestContext(request))

def spot_detail(request, spot_pk=None):
    spot = None
    if spot_pk is None:
        spot = Spot.objects.get_current_spot()
    else:
        spot = Spot.objects.get(pk=spot_pk)
    ctxt = {
        'spot':spot,
    }
    return render_to_response('radio_station/spot_detail.html', ctxt, context_instance=RequestContext(request))

def dj_detail(request, dj_slug):
    dj = get_object_or_404(DJ, slug=dj_slug)
    schedule = Schedule.objects.get_current_schedule(schedule)
    ctxt = {
        'dj':dj,
        'schedule':schedule,
    } 
    return render_to_response('radio_station/dj_detail.html', ctxt, context_instance=RequestContext(request))

def show_detail(request, show_slug):
    show = get_object_or_404(Show, slug=show_slug)
    schedule = Schedule.objects.get_current_schedule(schedule)
    ctxt = {
        'show':show,
        'schedule':schedule,
    } 
    return render_to_response('radio_station/show_detail.html', ctxt, context_instance=RequestContext(request))
