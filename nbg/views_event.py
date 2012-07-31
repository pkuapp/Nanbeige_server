# -*- coding: utf-8 -*-

from datetime import datetime
from django.db.models import Q
from django.core.exceptions import ValidationError
from nbg.models import Event, EventCategory
from nbg.helpers import json_response, auth_required

@json_response
def query(request):
    keyword =request.GET.get('keyword', None)
    category_id = request.GET.get('category_id', None)
    after = request.GET.get('after', datetime.now())
    before = request.GET.get('before', None)
    start = int(request.GET.get('start', 0))

    try:
        event_objs = Event.objects.filter(time__gte=after)
    except ValidationError:
        return {'error': 'after 日期格式错误。'}
    if keyword:
        event_objs = event_objs.filter(Q(title__contains=keyword)|Q(subtitle__contains=keyword))
    if category_id:
        event_objs = event_objs.filter(category=category_id)
    if before:
        try:
            event_objs = event_objs.filter(time__lte=before)
        except ValidationError:
            return {'error': 'before 日期格式错误。'}
    event_objs = event_objs[start:start+10]

    response = [{
        'id': item.pk,
        'title': item.title,
        'subtitle': item.subtitle,
        'category': {
            'id': item.category.pk,
            'name': item.category.name,
        },
        'time': item.time.isoformat(' '),
        'location': item.location,
        'follow_count': int(item.follow_count()),
    } for item in event_objs]

    return response

@json_response
def category(request):
    category_objs = EventCategory.objects.all()

    response = [{
        'id': category.pk,
        'name': category.name,
        'count': category.count(),
    } for category in category_objs]

    return response

@json_response
def get_event(request,offset):
    event_id = int(offset)
    
    event_obj = Event.objects.get(pk=event_id)
    response = {
        'id': event_obj.pk,
        'title': event_obj.title,
        'subtitle': event_obj.subtitle,
        'category_id': event_obj.category.pk,
        'category_name': event_obj.category.name,
        'location': event_obj.location,
        'organizer': event_obj.organizer,
        'content': event_obj.content,
        'follower_count': event_obj.follow_count(),
    }
    return response

@auth_required
@json_response
def follow(request):
    user = request.user
    event_id = request.GET.get('id', None)

    try:
        event = Event.objects.get(pk = event_id)
    except:
        return 'lack of neccessary parameter'

    if event.follower.filter(pk = user.id).count() > 0:
        pass
    else:
        event.follower.add(user)
        event.save()
    return 0

@auth_required
@json_response
def following(request):
    user = request.user
    event_objs = user.event_set.all()
    try:
        response = [{
            'id': item.pk,
            'title': item.title,
            'subtitle': item.subtitle,
            'category_id': item.category.pk,
            'category_name': item.category.name,
            'location': item.location,
            'organizer': item.organizer,
            'content': item.content,
            'follower_count': item.follow_count(),
        } for item in event_objs]

    except: 
        response = 'error'
    return response
