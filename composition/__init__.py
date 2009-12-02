from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from django.http import Http404, HttpResponseRedirect, HttpResponse
from django.template.loader import get_template

def compose_response(*functions):
    def composed_view(request, *args, **kwargs):
        context_out = {}
        for func in functions:
            output = func(request, *args, **kwargs)
            if isinstance(output, HttpResponse):
                return output
            context_out.update(output)
        return context_out
    return composed_view

def view_to_template(template):
    def templated_view(func):
        def call(request, *args, **kwargs):
            output = func(request, *args, **kwargs)
            if isinstance(output, HttpResponse):
                return output
            return render_to_response(template, output, context_instance=RequestContext(request))
        return call
    return templated_view


__all__ = ('compose_response', 'view_to_template') 
