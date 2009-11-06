from django.forms.widgets import TextInput
from django.utils import simplejson
from django.utils.safestring import mark_safe
from django.core.exceptions import ObjectDoesNotExist 

def fail_on_create(widget, datadict, name):
    """
        this is the default behavior for the autocomplete_input_factory
        just return None. If there's a success here we'd be returning a pk, but
        hey, whatever.
    """
    return None

def autocomplete_input_factory(model, url, function_list, instantiate=fail_on_create):
    class AutoCompleteWidget(TextInput):
        def __init__(self, *args, **kwargs):
            self.url = url
            self.function_list = function_list
            self.model = model
            self.instantiate = instantiate
            super(AutoCompleteWidget,self).__init__(*args, **kwargs)

        def value_from_datadict(self, data, files, name):
            value = super(AutoCompleteWidget, self).value_from_datadict(data, files, name)
            if value is not None and value != '':
                pk = None
                try:
                    obj = self.model.objects.get(name__exact=value)
                    pk = obj.pk
                except self.model.DoesNotExist:
                    pk = self.instantiate(self, data, name)
                return pk
            return None

        def render(self, name, value, attrs=None):
            real_value = ""
            if value is not None:
                try:
                    real_value = model.objects.get(pk__exact=value)
                except self.model.DoesNotExist:
                    real_value = value
            output = """
                %s
                <script type="text/javascript">
                    $(function () { 
                        $('input[name=%s]').autocomplete({"url":"%s", "query_functions":%s});
                    });
                </script>
            """ % (super(AutoCompleteWidget,self).render(name, real_value, attrs), name, self.url, simplejson.dumps(self.function_list))
            return mark_safe(output)

        class Media:
            js = ('site/js/jquery.js', 'site/js/autocomplete.js')
            css = { 'all': ['site/css/autocomplete.css',] }
    return AutoCompleteWidget
