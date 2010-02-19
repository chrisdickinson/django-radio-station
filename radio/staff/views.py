from django.core.urlresolvers import reverse
from django.db.models import Q
from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.template import RequestContext
from radio.station.models import Schedule
from .models import StaffRoleRelation
import datetime
def staff_list(request):
    now = datetime.datetime.now()
    current_schedule = Schedule.objects.get_current_schedule(now)
    return redirect(reverse('staff-list-for-schedule', kwargs={'schedule_pk':current_schedule.pk}))

def staff_list_for_schedule(request, schedule_pk):
    schedule = get_object_or_404(Schedule, pk=int(schedule_pk))
    query = Q(schedule__pk=schedule.pk)|Q(schedule__pk__isnull=True)
    roles = StaffRoleRelation.objects.filter(query).order_by('role__weight')
    context = {
        'schedule':schedule,
        'roles':roles,
    }
    return render_to_response('staff/staff_list.html', context, context_instance=RequestContext(request))
