# -*- coding: utf-8 -*-

from django.http import HttpResponse
from django.utils import simplejson
from nbg.models import *

def comment_list(request, offset):
    start = int(request.GET.get('start', None))
    if not start:
        start = 0
    comment_objs = Comment.objects[start : start+10]
    response = [{
        'id' : item.pk,
        'writer' : item.writer,
        'time' : item.time,
        'content' : item.content,
    }for item in comment_objs]
    return HttpResponse(simplejson.dumps(response), mimetype = 'application/json')
