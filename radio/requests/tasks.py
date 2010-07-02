def post_responses(requests):
    for request in requests:
        if request.dm_on_fulfilled:
            waiter = waiter.Waiter(menu_class=TwitterMenu, consumer=TwitterConsumer())
            waiter/"messages/create.json"/{
                'to_user':user.twitter.info.data.screen_name,
            }
