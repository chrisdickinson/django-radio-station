from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from django.http import Http404, HttpResponseRedirect, HttpResponse
from django.template.loader import get_template

def compose_response(**functions):
    def composed_view(request, *args, **kwargs):
        context_out = {}
        for func in functions:
            context_out.update(func(request, *args, **kwargs))
        return context_out
    return composed_view

def view_to_template(template):
    def templated_view(func):
        def call(request, *args, **kwargs):
            return render_to_response(template, func(request, *args, **kwargs), context_instance=RequestContext(request))
        return call
    return templated_view


__all__ = ('compose_response', 'view_to_template') 
