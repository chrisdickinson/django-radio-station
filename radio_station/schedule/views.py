from django.core.urlresolvers import reverse
from django.http import Http404, HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.utils import simplejson

from station.models import Schedule, Spot, Show, DJ
from generators import spot_dict_from_object, spot_generate_dicts
from controller import ScheduleController
from exceptions import BadSpotIncrement

SESSION_SPOTS_KEY = 'spots'

def grab_spot_dicts_for_schedule(schedule):
    spots = Spot.objects.filter(schedule=schedule)
    if spots:
        spots = [spot_dict_from_object(spot) for spot in spots]
    else:
        spots = None
    return spots

def get_spot_dicts(dictionary, schedule_pk):
    """
        get_spot_dicts(dictionary:dict, schedule_pk:int):
            a utility function that returns an array of spots as dictionary objects,
            or None if no spots exist in the dictionary.
                - it tries to grab them from the dictionary first, and if it can't
                  it tries to load them off the database. 
    """
    spots = None
    if SESSION_SPOTS_KEY in dictionary:
        spots = dictionary['spots']
    else:
        schedule_obj = Schedule.objects.get(pk__exact=schedule_pk)
        spots = grab_spot_dicts_for_schedule(schedule_obj)
    return spots

def generate_schedule(request, schedule_pk):
    schedule = get_object_or_404(Schedule, pk=int(schedule_pk))
    spots = Spot.objects.filter(schedule=schedule)
    if spots:
        raise Http404()
    context = {}
    response = None
    try:
        increment = request.POST['increment']
        spots = spot_generate_dicts(int(increment))
        request.session['spots'] = spots
        return HttpResponseRedirect(reverse('edit_schedule', kwargs={'schedule_pk':schedule_pk}))
    except BadSpotIncrement, e:
        context.update({
            'error':e
        })
    except KeyError, e:
        pass
    return render_to_response('station/schedule/admin/generate.html', context, context_instance=RequestContext(request))

def get_edit_schedule_context(request, spots):
    context = {}
    try:
        ctrl = ScheduleController(spots, request.POST)
        context.update({
            'controller':ctrl,
        })
    except Exception, e:
        context.update({
            'error_class':e.__class__.__name__,
            'error':str(e),
        })
    return context

def edit_schedule(request, schedule_pk):
    spots = None
    try:
        spots = get_spot_dicts(request.session, int(schedule_pk))
    except Schedule.DoesNotExist:
        raise Http404()

    if spots is None:
        return HttpResponseRedirect(reverse('generate_schedule', kwargs={'schedule_pk':schedule_pk}))

    context = get_edit_schedule_context(request, spots)
    if 'error' not in context.keys():
        request.session['spots'] = context['controller'].spots
    response = None
    if request.method == 'POST':
        response = HttpResponse(content=simplejson.dumps(context), mimetype='text/json')
    else:
        response = render_to_response('station/schedule/admin/edit.html',context, context_instance=RequestContext(request))
    return response
