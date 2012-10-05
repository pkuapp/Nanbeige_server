# -*- coding: utf-8 -*-

from datetime import datetime
from django.db.models import Q
from django.core.exceptions import ValidationError
from django.views.decorators.http import require_http_methods
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
        return {'error_code': 'SyntaxError'}, 400
    if keyword:
        event_objs = event_objs.filter(Q(title__contains=keyword)|Q(subtitle__contains=keyword))
    if category_id:
        event_objs = event_objs.filter(category=category_id)
    if before:
        try:
            event_objs = event_objs.filter(time__lte=before)
        except ValidationError:
            return {'error_code': 'SyntaxError'}, 400
    events = event_objs.select_related('category')[start:start+10]

    response = [{
        'id': event.pk,
        'title': event.title,
        'subtitle': event.subtitle,
        'category': {
            'id': event.category_id,
            'name': event.category.name,
        },
        'organizer': event.organizer,
        'time': event.time.isoformat(' '),
        'location': event.location,
        'content': event.content,
        'follower_count': int(event.follower_count()),
    } for event in events]

    return response

@json_response
def event(request,offset):
    id = int(offset)

    try:
        event = Event.objects.select_related('category').get(pk=id)
    except Event.DoesNotExist:
        return {'error_code': 'EventNotFound'}
    response = {
        'id': event.pk,
        'title': event.title,
        'subtitle': event.subtitle,
        'category': {
            'id': event.category_id,
            'name': event.category.name,
        },
        'organizer': event.organizer,
        'time': event.time.isoformat(' '),
        'location': event.location,
        'content': event.content,
        'follower_count': event.follower_count(),
    }
    return response

@json_response
def category(request):
    categories = EventCategory.objects.all()

    response = [{
        'id': category.pk,
        'name': category.name,
        'count': category.count(),
    } for category in categories]

    return response

@require_http_methods(['POST'])
@auth_required
@json_response
def edit(request, offset):
    id = int(offset)
    user = request.user
    follow = request.POST.get('follow', None)

    try:
        event = Event.objects.get(pk=id)
    except Event.DoesNotExist:
        return {'error_code': 'EventNotFound'}, 404

    if follow:
        if follow == '1':
            event.follower.add(user)
        elif follow == '0':
            event.follower.remove(user)
        else:
            return {'error_code': 'SyntaxError'}, 400

    event.save()

    return 0

@auth_required
@json_response
def following(request):
    events = request.user.event_set.all().select_related('category')

    response = [{
        'id': event.pk,
        'title': event.title,
        'subtitle': event.subtitle,
        'category': {
            'id': event.category_id,
            'name': event.category.name,
        },
        'organizer': event.organizer,
        'time': event.time.isoformat(' '),
        'location': event.location,
        'content': event.content,
        'follower_count': int(event.follower_count()),
    } for event in events]

    return response
