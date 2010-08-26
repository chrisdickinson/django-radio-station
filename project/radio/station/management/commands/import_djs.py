from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User, Group
from django.template.defaultfilters import slugify
from radio.station.models import DJ

import os
import sys
import random

word_list = [
    'partyparty',
    'beachhouse',
    'wavves',
    'garybusey',
    'norrit',
    'olympian',
    'blueish',
    'bbddm',
    'rooftop',
    'vigilantes',
    'naomi',
    'watt',
    'bandit',
    'teeth',
    'booandbootoo',
    'kitetails',
]

def mkpasswd(words):
    symbols = "!@#$%^&*(){}[]/?><,.';:\\|"
    numbers = range(0,10)
    randoms = [
        random.random()*len(symbols),
        random.random()*len(numbers),
        random.random()*len(words),
    ]
    randoms = [int(rand) for rand in randoms]
    passwd = [symbols[randoms[0]], str(numbers[randoms[1]]), words[randoms[2]]]
    random.shuffle(passwd)
    return ''.join(passwd)

class Command(BaseCommand):
    def handle(self, *args, **options):
        filename = args[0]
        group = Group.objects.get(name='DJs')
        keys = ['first', 'last', 'email']
        to_dict = lambda x: dict(zip(keys, x.strip().split(',')))
        out = []
        file = open(filename, 'r')
        lines = (to_dict(line) for line in file)
        for dj_dict in lines:
            unicode = False
            while not unicode:
                try:
                    dj_dict['email'] = u'%s'%dj_dict['email']
                    unicode = True
                except:
                    dj_dict['email'] = dj_dict['email'][:-1]
            try:
                User.objects.get(email=dj_dict['email'])
                print 'Skipping %s %s <%s> -- already exists.' % (dj_dict['first'], dj_dict['last'], dj_dict['email']) 
            except User.DoesNotExist:
                username = ''.join([dj_dict['first'].lower(), dj_dict['last'].lower()])
                user = User(username=username, email=dj_dict['email'], first_name=dj_dict['first'], last_name=dj_dict['last'], is_active=True, is_staff=True, is_superuser=False)
                passwd = mkpasswd(word_list)
                user.set_password(passwd)
                user.save()
                user.groups.add(group)
                user.save()
                out.append([username, passwd])
                dj = DJ(user=user)
                dj.display_name = dj_dict['first'] + ' ' + dj_dict['last'][0]
                dj.slug = slugify(username)
                dj.summary = 'DJ'
                dj.description = 'DJ'
                dj.save()
        for result in out:
            print result
        file.close()
