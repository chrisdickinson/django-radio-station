Array.prototype.has = function (elem) {
    for(var i = 0; i < this.length; ++i) {
        if(this[i] == elem) {
            return true;
        }
    }
    return false;
};

function startswith_json(obj, name_field) {
    var d = {};
    d[name_field+'__startswith']=$(obj).val();
    return d;
}

(function ($) {
    $.fn.autocomplete = function (options) {
        var timeout_fn = null;
        var obj = $(this);
        if(!options['name_field']) {
            options['name_field'] = 'name';
        }

        if(!(options.query_functions instanceof Array)) {
            options.query_functions = [options.query_functions];
        }

        var container_div = $('<div></div>').css({'position':'relative'});
        obj.parent().append(container_div);
        obj.appendTo(container_div);

        obj.attr('autocomplete', 'off');
        obj.parents('form').attr('autocomplete','off');
        var container = $('<ul />').addClass('autocomplete-container');
        obj.after(container);

        var waiting = false;

        var ask_server = function () {
            var build_suggestions = function (response) {
                waiting = false;
                if(response.length == 0) {
                    container.html('');
                    container.removeClass('autocomplete-visible');
                    container.parent().removeClass('autocomplete-parent-visible');
                } else {
                    var obj_val = obj.val();
                    var regex = new RegExp("("+obj_val+")(.*)"); 
                    var create_elem = function (pk, name) {
                        var bolded_name = name.replace(regex,"<strong>$1</strong>$2");
                        var elem = $('<li>'+bolded_name+'</li>');
                        elem.addClass('autocomplete-item');
                        elem.attr('pk', pk);
                        return elem;
                    };

                    var elems = $();
                    container.html('');
                    for(var i = 0; i < response.length; ++i) {
                        container.append(create_elem(response[i].pk, response[i][options.name_field]));
                    }
                    if(container.is(':hidden')) {
                        container.addClass('autocomplete-visible');
                        container.parent().addClass('autocomplete-parent-visible');
                    }
                }
            };

            var build_data = function () {
                data = {}
                for(var i = 0; i < options.query_functions.length; ++i) {
                    $.extend(data,
                    eval(options.query_functions[i]+"(obj, options.name_field)"));
                }
                return data;
            };
            $.getJSON(options.url, build_data(), build_suggestions);
            waiting = true;
        };

        var key_down = function (event) {
            if([38, 40, 13, 27].has(event.keyCode)) {
                if(event.shiftKey) {
                    return;
                }
                event.preventDefault();
            }
            if(container.is(':hidden')) {
                return;
            }
            var next_selected = function () {
                var sel = container.children('.autocomplete-selected').eq(0).next();
                if(sel.length == 0) {
                    sel = container.children('li:first-child');
                }
                container.children('li').removeClass('autocomplete-selected');
                sel.addClass('autocomplete-selected');
            };

            var prev_selected = function () {
                var sel = container.children('.autocomplete-selected').eq(0).prev();
                if(sel.length == 0) {
                    sel = container.children('li:last-child');
                }
                container.children('li').removeClass('autocomplete-selected');
                sel.addClass('autocomplete-selected');
            };

            var set_selected = function () {
                var selected = container.children('.autocomplete-selected').eq(0);
                container.html('').removeClass('autocomplete-visible');
                container.parent().removeClass('autocomplete-parent-visible');
                if(selected.length == 0) {
                    return;
                }
                obj.val(selected.text()).attr('pk', selected.attr('pk'));
            };
            switch(event.keyCode) {
                case 38:
                    prev_selected();
                    break;
                case 40:
                    next_selected();
                    break;
                case 13:
                    set_selected();
                    break;
                case 9:
                    set_selected();
                    break;
                case 27:
                    container.html('').removeClass('autocomplete-visible');
                    container.parent().removeClass('autocomplete-parent-visible');
                  break;
            }
        };

        var key_up = function (event) {
            if(timeout_fn) {
                clearTimeout(timeout_fn);
            }

            if(waiting) {
                return;
            }
            if(obj.val() == '') {
                container.html('').removeClass('autocomplete-visible');
                container.parent().removeClass('autocomplete-parent-visible');
                return;
            }
            if([38, 40, 9, 13, 27].has(event.keyCode)) {
                return;
            }

            timeout_fn = setTimeout(ask_server, 500);
        };
        obj.keyup(key_up).keydown(key_down).blur(function () {
                container.html('').removeClass('autocomplete-visible');
                container.parent().removeClass('autocomplete-parent-visible');
        });
    };
})(jQuery);
