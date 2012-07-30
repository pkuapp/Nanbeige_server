# -*- coding: utf-8 -*-

from nbg.models import Comment
from nbg.helpers import json_response, auth_required

@auth_required
@json_response
def comment_list(request):
    start = int(request.GET.get('start', 0))

    comment_objs = Comment.objects.all()[start:start+10]
    response = [{
        'id': item.pk,
        'writer': {
            'id': item.writer.pk,
            'nickname': item.writer.email,
        },
        'time': item.time.isoformat(' '),
        'content': item.content,
        'course': {
            'id': item.course.pk,
            'name': item.course.name,
        },
    } for item in comment_objs]
    return response
