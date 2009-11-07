(function ($) {
    $.fn.schedule = function (options) {
        var obj = $(this);
        var spots = options['spots'];
        var spot_objects = [];
        var dj_class = options['dj-class'];
        var spot_class = options['spot-class'];
        var show_class = options['show-class'];
        
        var SECONDS_IN_DAY = 60.0*60.0*24.0;

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
            var ratio_y = (obj.height()/SECONDS_IN_DAY);
            this.get_draggable_grid = function() {
                var grid_snap_y = parseInt(3600*ratio_y);
                return [0, grid_snap_y];
            };

            this.css_to_offset = function ($obj) {
                var from_top = parseInt($obj.css('top'));
                var offset = from_top / ratio_y;
                return parseInt(offset);
            };

            this.offset_to_css = function(spot) {
                var from_top = spot.offset * ratio_y;
                var from_left = spot.day_of_week * ratio_x;
                return {'top':parseInt(from_top)+'px', 'left':parseInt(from_left)+'px'};
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
                'overflow':'hidden',
                'border':'1px solid #333',
            };

            this.update = function(spot) {
                spot.dom.css(this.spot_chrome);
                spot.dom.css(graph.offset_to_css(spot));
                this.update_height(spot);
            };

            this.update_tops = function() {
                for(var i = 0; i < spot_objects.length; ++i) {
                    var spot = spot_objects[i];
                    spot.dom.css(graph.offset_to_css(spot));
                }
            };

            this.update_height = function(spot) {
                next = spot.dom.next('.weekday-'+spot.day_of_week);
                if(next.length > 0) {
                    var our_top = spot.dom.css('top');
                    var their_top = next.css('top');
                    var height = '100%';
                    if(their_top !== undefined) {
                        height = parseInt(their_top) - parseInt(our_top) - parseInt(next.css('paddingTop'));
                    }
                    spot.dom.css({'height':height+'px'});
                } else {
                    spot.dom.css({'height':'100%'});
                }
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
                for(var i in current_active_spot) {
                    fn(current_active_spot[i]);
                }
            }
        };

        function Spot(index, details) {
            var self = this;
            self.index = index;
            $.extend(this, details);
            this.dom = $('<div></div>').addClass(spot_class).addClass('weekday-'+self.day_of_week);

            var async_function = function(slot, attempt, complete) {
                self['attempt_'+slot] = function (event) { 
                    var results = attempt(event);
                    try {
                        var result = self.attempt_action(slot, results);
                        complete(result);
                    } catch (err) {
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
                                return return_value;
                           },
                           function (results) {
                                self.offset = results;
                                self.dom.children('.time').text(to_human_time(self.offset));
                                renderer.update(self);
                           });

            async_function('dj',
                           function(dj) {
                                var $dj = $(dj);
                                return $dj.data('pk');
                           },
                           function(results) {
                                self.dom.children('.dj').text($('#dj-'+results).text());
                                self.dj_pk = results;
                           });


            async_function('add',
                           function(event) {

                           },
                           function(results) {

                           });

            async_function('delete',
                            function(event) {

                            },
                            function(results) {

                            });

            async_function('repeat_every',
                            function(event) {

                            },
                            function(results) {

                            });

            this.keypress = function(event) {
                if(this.offset == 0) {
                    event.preventDefault();
                    return;
                }

                var delta = 900;
                if(event.shiftKey) {
                    delta *= 4;
                }
                var offset = self.offset;
                if(event.keyCode == 38) {
                    offset -= delta;
                }
                else if(event.keyCode == 40) {
                    offset += delta;
                }
                self.attempt_offset({'type':'keyOff', 'offset':offset});
                event.preventDefault();
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
                    self.dom.bind('dragstop', function(event, ui) {
                        self.attempt_offset(event);
                        self.dom.unbind('dragstop');
                    });
                });
            }

            self.dom.addClass('dj-dropzone');
            self.dom.droppable({
                'accept':'.dj',
                'drop':function (event) {
                    self.attempt_dj(event.originalTarget);
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

            this.dom.append('<span class="time">'+to_human_time(this.offset)+'</span>');
            this.dom.append(' - <span class="dj"></span>');
            this.dom.append(' - <span class="show"></span>');
            obj.append(this.dom);
        };


        for (var i = 0; i < spots.length; ++i) {
            var spot = new Spot(i, spots[i]);
            spot_objects.push(spot);
        }
        renderer.update_tops();
        for(var i = 0; i < spot_objects.length; ++i) {
            renderer.update(spot_objects[i]);
        }

        var delegate_keypress = function (event) {
            if(event.keyCode == 27) {
                apply_to_active_spots('blur', event, function (s) { s.dom.removeClass('active'); }); 
            }
            apply_to_active_spots('keypress', event); 
        };

        $(document).bind('keydown', delegate_keypress);
    }
})(jQuery);

(function ($) {
    $.fn.obj_list = function (options) {
        var obj = $(this);
        var obj_callback = function (data) {
            obj.html('');
            for(var i in data) {
                var obj_data = data[i];
                var display_title = options.display(obj_data);
                var pk = options.primary_key(obj_data);
                var $dom = $('<li>'+display_title+'</li>');
                $dom.addClass(options['class']).draggable({
                    'revert':true,
                });
                $dom.data('pk', obj_data['id']);
                $dom.attr('id', options['class']+'-'+obj_data['id']);
                obj.append($dom);
            }
        };
        $.getJSON(options['url'], {}, obj_callback);
    };
})(jQuery);

