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
        return {'error': 'after 日期格式错误。'}, 400
    if keyword:
        event_objs = event_objs.filter(Q(title__contains=keyword)|Q(subtitle__contains=keyword))
    if category_id:
        event_objs = event_objs.filter(category=category_id)
    if before:
        try:
            event_objs = event_objs.filter(time__lte=before)
        except ValidationError:
            return {'error': 'before 日期格式错误。'}, 400
    event_objs = event_objs.select_related('category')[start:start+10]

    response = [{
        'id': item.pk,
        'title': item.title,
        'subtitle': item.subtitle,
        'category': {
            'id': item.category_id,
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
    id = int(offset)

    event = Event.objects.select_related('category').get(pk=id)
    response = {
        'id': event.pk,
        'title': event.title,
        'subtitle': event.subtitle,
        'category': {
            'id': event.category_id,
            'name': event.category.name,
        },
        'location': event.location,
        'organizer': event.organizer,
        'content': event.content,
        'follower_count': event.follow_count(),
    }
    return response

@require_http_methods(['POST'])
@auth_required
@json_response
def follow(request, offset):
    id = int(offset)
    user = request.user

    try:
        event = Event.objects.get(pk=id)
    except Event.DoesNotExist:
        return {'error': '活动不存在。'}, 404

    event.follower.add(user)
    event.save()

    return 0

@auth_required
@json_response
def following(request):
    events = request.user.event_set.all().select_related('category')

    response = [{
        'id': item.pk,
        'title': item.title,
        'subtitle': item.subtitle,
        'category': {
            'id': item.category_id,
            'name': item.category.name,
        },
        'location': item.location,
        'organizer': item.organizer,
        'content': item.content,
        'follower_count': item.follow_count(),
    } for item in events]

    return response
