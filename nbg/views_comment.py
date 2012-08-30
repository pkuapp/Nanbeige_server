# -*- coding: utf-8 -*-

from nbg.models import Comment
from nbg.helpers import json_response, auth_required

@auth_required
@json_response
def comment_list(request):
    # TODO: need optimization
    start = int(request.GET.get('start', 0))

    courses = request.user.get_profile().courses.all()
    comments = Comment.objects.filter(course__in=courses)[start:start+10]

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
    } for item in comments]
    return response
