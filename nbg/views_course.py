# -*- coding:UTF-8 -*-

from django.http import HttpResponse
from django.utils import simplejson

def course_list(request):
    course_values = Course.objects.values()
    response = [{
        'id': item.id,
        'orig_id': item.original_id',
        'name': item.name,
        'credit': item.credit,
    } for item in course_values]
    return HttpResponse(simplejson.dumps(response), mimetype='application/json')

def assignment_list(request):
    return HttpResponse(simplejson.dumps({'xxx': 'yyy'}),mimetype='application/json')
