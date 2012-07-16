# -*- coding:UTF-8 -*-
from django.shortcuts import *
from django.template import RequestContext
from django.http import HttpResponse

from nbg.models import *
from django.contrib import auth
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.utils import simplejson
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from datetime import datetime

def query(request):
    keyword =request.GET.get('keyword', None)
    category_id = request.GET.get('category_id',None)
    after = request.GET.get('after', None)
    before = request.GET.get('before',None)
    start = request.GET.get('start', None)
    batch = request.GET.get('batch', None)

    event_objs = Event.objects.all()
    if keyword:
        event_objs = event_objs.filter(title__contains = keyword())
    if category_id:
        event_objs = event_objs.filter(category = category_id())
    if after:
        event_objs = event_objs.filter(time__gte = datetime.fromtimestamp(float(after)))
    else:
        event_objs = event_objs.filter(time__gte = datetime.now())
    if before:
        event_objs = event_objs.filter(time__lte = datetime.fromtimestamp(float(before)))
    if not start:
        start = 0
    if not batch:
        batch =10
    event_objs = event_objs[int(start):int(batch)]

    event_values = event_objs.values()
    for i in range(len(event_values)):
        event_values[i]['time']  = event_values[i]['time'].isoformat(' ')
        event_values[i]['category_name'] = EventCategory.objects.get(pk = event_values[i])
        event_values[i]['follower_count'] = int(event_objs[i].follow_count())
    return HttpResponse(simplejson.dumps(list(event_values)),mimetype = 'application/json')

def category(request):
    category_objs = EventCategory.objects.all()
    category_values = list(category_objs.values())

    for i in range(len(category_values)):
        category_values[i]['count'] = category_values[i].count()
    return HttpResponse(simplejson.dumps(list(category_values)),mimetype = 'application/json')

def get(request):
    event_id = request.GET.get('id',None)

    if event_id:
        try:
            event_queryset = Event.objects.filter(pk = int(event_id))
            event_objs = event_queryset[0]
            event = event_queryset.values()[0]
            event['time']  = event['time'].isoformat(' ')
            event['category_name'] = EventCategory.objects.get(pk = event['category_id'].name)
            event['follow_count'] = int(event_objs.follow_count())
            return HttpResponse(simplejson.dumps(list(event)),mimetype = 'application/json')
        except:
            return HttpResponse(simplejson.dumps('lack of neccessary parameter'),mimetype = 'application/json')
    else:
        return HttpResponse(simplejson.dumps(list('invalid type-in')),mimetype = 'application/json')

def follow(request):
    user = request.user
    event_id = request.GET.get('id', None)

    try:
        event = Event.objects.get(pk = event_id)
    except:
        return HttpResponse(simplejson.dumps('lack of neccessary parameter'),mimetype = 'application/json')

    if event.follower.filter(pk = user.id).count() > 0:
        pass
    else:
        event.follower.add(user)
        event.save()
    return HttpResponse('0')

def following(request):
    user = request.user

    event_objs = user.event_set.all()
    event_values = event_objs.values()
    for i in range(len(event_values)):
        event_values[i]['time'] = event_values[i]['time'].isoformat(' ')
        event_values[i]['category_name'] = EventCategory.objects.get(pk = event_values[i]('category_id')).name
        event_values[i]['follow_count'] = int(event_objs[i].follow_count())
    return HttpResponse(simplejson.dumps(list(event_values)),mimetype = 'application/json')