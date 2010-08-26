Array.prototype.has = function (obj) {
    for(var i = 0; i < this.length; ++i) {
        if(this[i] == obj) {
            return true;
        }
    }
    return false;
};

(function ($) {
    $.fn.schedule = function (options) {
        var obj = $(this);
        var spots = options['spots'];
        var spot_objects = [];
        var dj_class = options['dj-class'];
        var dj_class_dot = '.'+dj_class;
        var spot_class = options['spot-class'];
        var show_class = options['show-class'];
        var show_class_dot = '.'+show_class;
        var deleted_existing_pks = [];        
        var SECONDS_IN_DAY = 60.0*60.0*24.0;

        var multiplier = 1.0;
        var mul_max = 6.0;
        var mul_min = 0.5;


        var to_human_time = function(offset) {
            var hours = parseInt(offset / 3600);
            var minutes = parseInt((offset % 3600) / 60);
            var ampm = hours > 12 ? 'pm' : 'am';
            if(ampm == 'pm') { hours -= 12; }
            if(hours == 0) { hours = 12; }
            if(minutes < 10) { minutes = '0'+minutes; }
            return hours+':'+minutes+ampm;
        };

        function Graph () {
            var ratio_x = (obj.width()/7.0);
            var ratio_y = ((obj.height())/SECONDS_IN_DAY);
            this.get_draggable_grid = function() {
                var grid_snap_y = parseInt(3600*ratio_y);
                return [0, grid_snap_y];
            };

            this.css_to_offset = function ($obj) {
                var from_top = parseInt($obj.css('top'));
                var offset = from_top / (ratio_y * multiplier);
                return parseInt(offset);
            };

            this.offset_to_px = function(offset) {
                var from_top = offset * ratio_y;
                return parseInt(from_top * multiplier);
            };

            this.day_of_week_to_px = function(day_of_week) {
                var from_left = day_of_week * ratio_x;
                return from_left;
            };

            this.offset_to_css = function(spot) {
                return {'top':this.offset_to_px(spot.offset)+'px', 'left':this.day_of_week_to_px(spot.day_of_week)+'px'};
            };
        };
        var graph = new Graph();

        var renderer = null;
        function Renderer () {
            this.spot_chrome = {
                'position':'absolute',
                'width':parseInt(obj.width()/7.0-1)+'px',
            };

            this.container_chrome = {
                'position':'relative',
                'border':'1px solid #333',
            };

            this.update = function(spot, and_previous) {
                spot.dom.css(this.spot_chrome);
                spot.dom.css(graph.offset_to_css(spot));
                this.update_height(spot);
                spot.dom.find('.time').text(to_human_time(spot.offset));
                spot.dom.find(dj_class_dot).text($('#dj-'+spot.dj_pk).text());
                spot.dom.find(show_class_dot).text($('#show-'+spot.show_pk).text());

                if(![spot.show_pk, spot.dj_pk].has(-1)) {
                    spot.dom.addClass('complete');
                } else {
                    spot.dom.removeClass('complete');
                }
                if(and_previous) {
                    var prev_spot = spot_objects[spot_objects.indexOf(spot)-1];
                    if(prev_spot === undefined) {
                    } else {
                        this.update(prev_spot);
                    } 
                } 
            };

            this.update_tops = function() {
                for(var i = 0; i < spot_objects.length; ++i) {
                    var spot = spot_objects[i];
                    spot.dom.css(graph.offset_to_css(spot));
                }
            };

            this.update_height = function(spot) {
                next = spot.dom.next('.weekday-'+spot.day_of_week);
                var height = '100%';
                var our_top = spot.dom.css('top');
                if(next.length > 0) {
                    var their_top = next.css('top');
                    if(their_top !== undefined) {
                        height = parseInt(their_top) - parseInt(our_top) - parseInt(next.css('paddingTop'));
                    } else {
                        height = (graph.offset_to_px(SECONDS_IN_DAY) - parseInt(our_top));
                    }
                } else {
                    height = (graph.offset_to_px(SECONDS_IN_DAY) - parseInt(our_top));
                }
                spot.dom.css({'height':height+'px'});
            };

            this.initialize = function() {
                obj.css(this.container_chrome);
            };
        }; 
        renderer = new Renderer();
        var current_active_spot = null;
        renderer.initialize();

        var apply_to_active_spots = function(name, event, wrap) {
            var fn = function (spot) {
                if(wrap) {
                    wrap(spot);
                }
                if(spot[name]) {
                    spot[name](event);
                }
            };
            if(current_active_spot !== null) {
                for(var i = 0; i < current_active_spot.length; ++i) {
                    fn(current_active_spot[i]);
                }
            }
        };

        function Spot(details) {
            var self = this;
            $.extend(this, details);
            this.dom = $('<div></div>').addClass(spot_class).addClass('weekday-'+self.day_of_week);

            var async_function = function(slot, attempt, complete) {
                self['attempt_'+slot] = function (event) { 
                    try {
                        var results = attempt(event);
                        results = self.attempt_action(slot, results);
                        complete(results);
                    } catch (err) {
                        renderer.update(self);
                    }
                };
            };

            async_function('offset',
                           function (event) {
                                var return_value = self.offset;
                                if (event.type == 'keyOff') {
                                    return_value = event.offset;
                                } else {
                                    return_value = graph.css_to_offset(self.dom);
                                }
                                return_value = parseInt(Math.round(return_value/900)) * 900;

                                var prev = self.dom.prev('.weekday-'+self.day_of_week);
                                var prev_offset = 0;
                                if(prev.length > 0) {
                                    prev_offset = graph.css_to_offset(prev);
                                }
                                if(return_value < prev_offset) {
                                    throw "Not allowed!";   
                                }
                                var next = self.dom.next('.weekday-'+self.day_of_week);
                                var next_offset = self.dom.parent().height();
                                if(next.length > 0) {
                                    next_offset = graph.css_to_offset(next);
                                }
                                if(return_value > next_offset) {
                                    self.dom.animate(graph.offset_to_css(self),200);
                                    throw "Not allowed!";   
                                }

                                return return_value;
                           },
                           function (results) {
                                self.offset = results;
                                renderer.update(self, true);
                           });

            async_function('dj',
                           function(dj) {
                                var $dj = $(dj);
                                return $dj.data('pk');
                           },
                           function(results) {
                                self.dj_pk = results;
                                renderer.update(self);
                           });

            async_function('show',
                           function(show) {
                                var $show = $(show);
                                return $show.data('pk');
                           },
                           function(results) {
                                self.show_pk = results;
                                renderer.update(self);
                           });

            async_function('add',
                           function(event) {
                                var $next = self.dom.next('.weekday-'+self.day_of_week);
                                var next_offset = SECONDS_IN_DAY;
                                if($next.length > 0) {
                                    next_offset = graph.css_to_offset($next);
                                }
                                var new_offset = parseInt((next_offset - self.offset) / 2.0) + self.offset;
                                new_offset = parseInt(Math.round(new_offset/900)) * 900;
                                if([next_offset, self.offset].has(new_offset)) {
                                    throw "Not enough room for a new spot!";
                                }
                                return new_offset;
                           },
                           function(results) {
                                var new_spot = new Spot({
                                    'pk':-1,
                                    'dj_pk':-1,
                                    'show_pk':-1,
                                    'repeat_every':0,
                                    'day_of_week':self.day_of_week,
                                    'offset':results
                                });
                                spot_objects.splice(spot_objects.indexOf(self),0,new_spot);
                                self.dom.after(new_spot.dom);
                                renderer.update(new_spot);
                                renderer.update(self);
                            });

            async_function('delete',
                            function(event) {
                                if(self.offset == 0) {
                                    throw "Cannot delete the first spot on a day.";
                                }
                                return true;
                            },
                            function(results) {
                                self.dom.remove();
                                var our_index = spot_objects.indexOf(self);
                                if(self.pk != -1) {
                                    deleted_existing_pks.push(self.pk);
                                }
                                spot_objects.splice(our_index, 1);
                                renderer.update(spot_objects[our_index-1]);
                            });

            async_function('repeat_every',
                            function(event) {

                            },
                            function(results) {

                            });

            this.keypress = function(event) {
                var delta = 900;
                if(event.shiftKey) {
                    delta *= 4;
                }
                var offset = self.offset;
                if([38, 40].has(event.keyCode)) {
                    if(this.offset == 0) {
                        event.preventDefault();
                        return;
                    }
                    if(event.keyCode == 38) {
                        offset -= delta;
                    }
                    else if(event.keyCode == 40) {
                        offset += delta;
                    }
                    self.attempt_offset({'type':'keyOff', 'offset':offset});
                    event.preventDefault();
                } else if ([8].has(event.keyCode)) {
                    self.attempt_delete(event);
                } else if ([65].has(event.keyCode)) {
                    self.attempt_add(event);
                }
            };

            this.focus = function (event) {

            };

            this.blur = function (event) {

            };

            this.attempt_action = function(action, values) {
                return values;
            };

            this.dom.click(function (event) {
                if(event.ctrlKey || event.metaKey) {
                    if(current_active_spot === null) {
                        current_active_spot = []
                    }
                    current_active_spot.push(self);
                } else {
                    apply_to_active_spots('blur', event, function (s) { s.dom.removeClass('active'); }); 
                    current_active_spot = [self];
                }
                $(this).addClass('active');
            });
            

            if(this.offset > 1) {
                this.dom.draggable({
                    'axis':'y',
                    'grid':graph.get_draggable_grid(),
                });

                this.dom.bind('dragstart', function (event, ui) {
                    self.dom.css({'height':'100%'});
                    self.dom.bind('dragstop', function(event, ui) {
                        self.attempt_offset(event);
                        self.dom.unbind('dragstop');
                    });
                });
            }

            self.dom.addClass('dj-dropzone');
            self.dom.droppable({
                'accept':'li',
                'drop':function (event, ui) {
                    classes = $(ui.draggable).attr('class').split(' ');
                    if(classes.has(dj_class)) {
                        self.attempt_dj(ui.draggable);
                    } else if(classes.has(show_class)) {
                        self.attempt_show(ui.draggable);
                    }
                    $('.hovered').removeClass('hovered');
                },
                'over':function(event) {
                    self.dom.addClass('hovered');
                },
                'out':function(event) {
                    self.dom.removeClass('hovered');
                },
                'tolerance':'pointer'
            });

            this.create_controls = function () {
                var container = $('<div></div>');
                container.append($('<span />').addClass('time'));
                container.append($('<span />').addClass('dj'));
                container.append($('<span />').addClass('show'));
                container.addClass('spot-container');

                var controls = $('<div></div>').addClass('spot-controls');
                controls.append($('<a href="#">add spot after</a>').click(function (event) {
                    event.preventDefault();
                    self.attempt_add();
                }));
                controls.append($('<a href="#">remove spot</a>').click(function (event) {
                    event.preventDefault();
                    self.attempt_delete();
                }));
                controls.append($('<a href="#">edit repeat</a>').click(function (event) {
                    event.preventDefault();
                    self.attempt_repeat_every();
                }));
                container.append(controls);
                return container;
            };
            this.dom.append(this.create_controls());
            this.output = function (i) {
                    var out = {};
                    out['offset'+i]=self.offset;
                    out['day_of_week'+i]=self.day_of_week;
                    out['repeat_every'+i]=self.repeat_every;
                    out['show_pk'+i]=self.show_pk;
                    out['dj_pk'+i]=self.dj_pk;
                    out['pk'+i]=self.pk;
                    return out;
                };
        };


        for (var i = 0; i < spots.length; ++i) {
            var spot = new Spot(spots[i]);
            obj.append(spot.dom);
            spot_objects.push(spot);
        }

        
        var rerender = function () {
            renderer.update_tops();
            for(var i = 0; i < spot_objects.length; ++i) {
                renderer.update(spot_objects[i]);
            }
        }
        rerender();

        var delegate_keypress = function (event) {
            if(current_active_spot) {
                if(event.keyCode == 27) {
                    apply_to_active_spots('blur', event, function (s) { s.dom.removeClass('active'); }); 
                    current_active_spot = null;
                }
                apply_to_active_spots('keypress', event);
            } 
            if(event.keyCode == 8) {
                if(!$(event.originalTarget).is(':input')) {
                    event.preventDefault();
                }
            }
            if(event.shiftKey) {
                if(event.keyCode == 0) {
                    multiplier -= 0.5;
                } else if (event.keyCode == 107) {
                    multiplier += 0.5;
                }
                if(multiplier > mul_max) multiplier = mul_max;
                if(multiplier < mul_min) multiplier = mul_min;

                rerender();
            }
            console.log(event.keyCode);
        };

        if(options['apply_to_all_id']) {
            var apply_to_all = $(options['apply_to_all_id']);
            apply_to_all.droppable({
                'accept':'li',
                'drop':function (event, ui) {
                    classes = $(ui.draggable).attr('class').split(' ');
                    var fn = null;
                    if(classes.has(dj_class)) {
                        apply_to_active_spots('attempt_dj', ui.draggable);
                    } else if(classes.has(show_class)) {
                        apply_to_active_spots('attempt_show', ui.draggable);
                    }
                    $('.hovered').removeClass('hovered');
                },
                'over':function(event) {
                    $(this).addClass('hovered');
                },
                'out':function(event) {
                    $(this).removeClass('hovered');
                },
                'tolerance':'pointer'
            });
        }
        if(options['controls']) {
            var controls = $(options['controls']);
            var save_schedule = $('<a href="#">Save</a>');
            var attempt_save = function(event) {
                event.preventDefault();
                var loc = '' + document.location;
                loc = loc.replace('http://', '');
                loc = loc.split('/');
                var home = loc.splice(0,1);
                loc = '/'+loc.join('/');
                var spots_out = {} 
                for(var i = 0; i < spot_objects.length; ++i) {
                    $.extend(spots_out, spot_objects[i].output(i));
                }
                spots_out['num'] = spot_objects.length;
                spots_out['deleted'] = deleted_existing_pks;

                var get_response = function (results) {
                    results = eval('('+results+')');
                    if(results.status == 'ok') {
                        document.location = 'http://' + home + results.redirect;
                    } else {
                    }
                };
                $.post(loc, spots_out, get_response);
            };
            save_schedule.click(attempt_save);
            controls.append(save_schedule);
        }
        $(document).bind('keydown', delegate_keypress);
    }
})(jQuery);

(function ($) {
    $.fn.obj_list = function (options) {
        var obj = $(this);
        var obj_callback = function (data) {
            obj.html('');
            for(var i = 0; i < data.length; ++i) {
                var obj_data = data[i];
                var display_title = options.display(obj_data);
                var pk = options.primary_key(obj_data);
                var $dom = $('<li>'+display_title+'</li>');

                var clone_fn = function(event) {
                    var clone = $(this).clone();
                    clone.data('pk', $(this).data('pk'));
                    clone.data('pk', $(this).data('pk'));
                    clone.addClass('cloned-li');
                    return clone;
                };

                $dom.addClass(options['class']).draggable({
                    'revert':true,
                    'appendTo':'body',
                    'helper':clone_fn,
                });
                $dom.data('pk', obj_data['id']);
                $dom.attr('id', options['class']+'-'+obj_data['id']);
                obj.append($dom);
            }
            if(options['on_finish']) {
                options['on_finish']();
            }
        };
        $.getJSON(options['url'], {'page_by':30000}, obj_callback);
        if(options['search']) {
            var search = $(options['search']);
            var on_keypress = function (event) {
                var our_text = search.val();
                if(our_text.length > 0) {
                    obj.find('li:not(:contains('+our_text+'))').hide();
                    obj.find('li:contains('+our_text+')').show();
                } else {
                    obj.find('li').show();
                }
            };
            var a_button = $('<a href="#">clear</a>').addClass('deletelink').css({
                'paddingLeft':'15px',
                'marginLeft':'10px'
            });
            a_button.click(function(event) {
                search.val(''); obj.find('li').show();
                event.preventDefault();
            });
            search.after(a_button);
            search.keyup(on_keypress);
        }
    };
})(jQuery);

