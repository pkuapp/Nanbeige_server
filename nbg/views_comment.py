# -*- coding: utf-8 -*-

from django.http import HttpResponse
from django.utils import simplejson
from nbg.models import Comment

def comment_list(request):
    start = int(request.GET.get('start', 0))

    comment_objs = Comment.objects.all()[start:start+10]
    response = [{
        'id': item.pk,
        'writer': {
            'id': item.writer.pk,
            'nickname': item.writer.email,
        },
        'time': item.time.isoformat(),
        'content': item.content,
        'course': {
            'id': item.course.pk,
            'name': item.course.name,
        },
    } for item in comment_objs]
    return HttpResponse(simplejson.dumps(response), mimetype = 'application/json')
