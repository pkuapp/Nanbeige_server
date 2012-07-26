# -*- coding: utf-8 -*-

from django.http import HttpResponse
from django.utils import simplejson
from datetime import datetime
from nbg.models import Event, EventCategory

def query(request):
    keyword =request.GET.get('keyword', None)
    category_id = request.GET.get('category_id', None)
    after = request.GET.get('after', None)
    before = request.GET.get('before', None)
    start = request.GET.get('start', None)
    batch = request.GET.get('batch', None)

    event_objs = Event.objects.all()
    if keyword:
        event_objs = event_objs.filter(title__contains=keyword)
    if category_id:
        event_objs = event_objs.filter(category=category_id)
    if after:
        event_objs = event_objs.filter(time__gte=datetime.fromtimestamp(float(after)))
    else:
        event_objs = event_objs.filter(time__gte=datetime.now())
    if before:
        event_objs = event_objs.filter(time__lte=datetime.fromtimestamp(float(before)))
    if not start:
        start = 0
    if not batch:
        batch = 10
    event_objs = event_objs[int(start):int(batch)]

    response = [{
        'id': item.pk,
        'title': item.title,
        'subtitle': item.subtitle,
        'category_id': item.category.pk,
        'category_name': item.category.name,
        'time': item.time.isoformat(' '),
        'location': item.location,
        'follow_count': int(item.follow_count()),
    } for item in event_objs]

    return HttpResponse(simplejson.dumps(response), mimetype='application/json')

def category(request):
    category_objs = EventCategory.objects.all()

    response = [{
        'id': category.pk,
        'name': category.name,
        'count': category.count(),
    } for category in category_objs]

    return HttpResponse(simplejson.dumps(response), mimetype='application/json')

def get_event(request,offset):
    event_id = int(offset)
    
    event_obj = Event.objects.get(pk=event_id)
    response = {
        'id' : event_obj.pk,
        'title' : event_obj.title,
        'subtitle' : event_obj.subtitle,
        'category_id' : event_obj.category.pk,
        'category_name' : event_obj.category.name,
        'location' : event_obj.location,
        'organizer' : event_obj.organizer,
        'content' : event_obj.content,
        'follower_count' : event_obj.follow_count(),
    }
    return HttpResponse(simplejson.dumps(response), mimetype='application/json')

def follow(request):
    user = request.user
    event_id = request.GET.get('id', None)

    try:
        event = Event.objects.get(pk = event_id)
    except:
        return HttpResponse(simplejson.dumps('lack of neccessary parameter'), mimetype='application/json')

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
        event_values[i]['category_name'] = EventCategory.objects.get(pk=event_values[i]('category_id')).name
        event_values[i]['follow_count'] = int(event_objs[i].follow_count())
    return HttpResponse(simplejson.dumps(list(event_values)), mimetype='application/json')
