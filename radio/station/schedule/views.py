from django.core.urlresolvers import reverse
from django.http import Http404, HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.utils import simplejson
from django.utils.safestring import mark_safe
from django.core.exceptions import PermissionDenied
from radio.station.models import Schedule, Spot, Show, DJ
from generators import spot_dict_from_object, spot_generate_dicts, spot_object_from_dict, spot_dicts_from_schedule
from controller import ScheduleController
from exceptions import BadSpotIncrement
from forms import GenerateScheduleForm, CopyScheduleForm
from composition import *

def must_have_perm(request, *args, **kwargs):
    if not request.user.has_perm(Schedule._meta.get_change_permission()):
        raise PermissionDenied
    return {}

def edit_existing_schedule(request, schedule_pk):
    if not request.user.has_perm(Schedule._meta.get_change_permission()):
        raise PermissionDenied
    schedule = get_object_or_404(Schedule, pk=schedule_pk)
    spot_dicts = spot_dicts_from_schedule(schedule)
    request.session['spots'] = spot_dicts
    return HttpResponseRedirect(reverse('admin:edit_schedule', kwargs={'schedule_pk':schedule_pk}))
edit_existing_schedule = compose_response(must_have_perm, edit_existing_schedule)

def generate_schedule(request, schedule_pk):
    if not request.user.has_perm(Schedule._meta.get_change_permission()):
        raise PermissionDenied
    response = None
    generate_form = GenerateScheduleForm() 
    copy_form = CopyScheduleForm()
    try:
        if request.method == 'POST':
            generate_form = GenerateScheduleForm(request.POST)
            copy_form = CopyScheduleForm(request.POST)
            spot_dicts = None
            if generate_form.is_valid() and generate_form.cleaned_data['increment']:
                dj = generate_form.cleaned_data['default_dj']
                if dj:
                    dj = DJ.objects.get(pk=dj)
                else:
                    dj = None
                show = generate_form.cleaned_data['default_show']
                if show:
                    show = Show.objects.get(pk=show)
                else:
                    show = None
                spot_dicts = spot_generate_dicts(int(generate_form.cleaned_data['increment']), dj, show)
            elif copy_form.is_valid():
                schedule = Schedule.objects.get(pk=generate_form['schedule'])
                spot_dicts = spot_dicts_from_schedule(schedule, {
                    'pk':-1,
                })
            request.session['spots'] = spot_dicts
            return HttpResponseRedirect(reverse('admin:edit_schedule', kwargs={'schedule_pk':schedule_pk}))
    except Schedule.DoesNotExist:
        pass
    except DJ.DoesNotExist:
        pass
    except Show.DoesNotExist:
        pass
    if response is None:
        context = {
            'schedule':get_object_or_404(Schedule, pk=schedule_pk),
            'generate_form':generate_form,
            'copy_form':copy_form,
        }
        response = render_to_response('station/admin/generate.html', context, context_instance=RequestContext(request))
    return response 

def get_spots_from_post(post):
    num = int(post.get('num', 0))
    spots = []
    for i in range(0, num):
        spots.append({
            'offset':int(post.get('offset%d'%i)),
            'dj_pk':int(post.get('dj_pk%d'%i)),
            'show_pk':int(post.get('show_pk%d'%i)),
            'pk':int(post.get('pk%d'%i)),
            'repeat_every':int(post.get('repeat_every%d'%i)),
            'day_of_week':int(post.get('day_of_week%d'%i)),
        })
    return spots


def edit_schedule(request, schedule_pk):
    if not request.user.has_perm(Schedule._meta.get_change_permission()):
        raise PermissionDenied
    schedule = get_object_or_404(Schedule, pk=schedule_pk)
    spots = request.session.get('spots', None)
    if spots is None:
        return HttpResponseRedirect('admin:generate_schedule', kwargs={'schedule_pk':schedule_pk})
    if request.method == 'POST':
        try:
            spots = get_spots_from_post(request.POST)
            deleted_spots = request.POST.getlist('deleted')
            spot_objects = []
            for spot in spots:
                spot_object = None
                if spot.get('pk', None) in (None, -1):
                    spot_object = spot_object_from_dict(spot)
                else:
                    spot_object = Spot.objects.get(pk=spot['pk'])
                    for attr in spot:
                        if attr == 'pk':
                            continue
                        attr_val = int(spot[attr])
                        if attr == 'show_pk':
                            attr = 'show'
                            attr_val = Show.objects.get(pk=attr_val)
                        if attr == 'dj_pk':
                            attr = 'dj'
                            attr_val = DJ.objects.get(pk=attr_val)
                        setattr(spot_object, attr, attr_val)
                spot_objects.append(spot_object)
            for spot_object in spot_objects:
                spot_object.schedule = schedule
                spot_object.save()
           
            if deleted_spots:
                Spot.objects.filter(pk__in=[int(spot) for spot in deleted_spots]).delete()
            request.user.message_set.create(message="Updated schedule.")
            request.session['spots'] = []
            response = {
                'status':'ok',
                'redirect':reverse('admin:station_schedule_changelist'),
            }
        except (Show.DoesNotExist, DJ.DoesNotExist, Spot.DoesNotExist):
            response = {
                'status':'error',
                'message':'there was an error'
            }
        return HttpResponse(simplejson.dumps(response), mimetype='text/json')
    else:
        ctxt = {
            'schedule':schedule,
            'spots':mark_safe(simplejson.dumps(spots)),
        }
        return render_to_response('station/admin/edit_spots.html', ctxt, context_instance=RequestContext(request))
