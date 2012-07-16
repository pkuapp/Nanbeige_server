# -*- coding:UTF-8 -*-
from django.http import HttpResponse
from django.utils import simplejson
from nbg.models import *


def course_list(request):
    course_values = Course.objects.values()
    response = [{
        'id' : item.id,
        'orig_id' : item.original_id,
        'name' : item.name,
        'credit' : item.credit,
        'teacher' : item.teacher__set.all(),
        'ta' : item.ta__set.all(),
        'week' : item.week__set(),
        'lessons': [{
            'day': lesson.day,
            'start' : lesson.start,
            'end' : lesson.end,
            'location' : lesson.location,
        } for lesson in item.lesson__set.all()]
    } for item in course_values]
    return HttpResponse(simplejson.dumps(response), mimetype='application/json')

def assignment_list(request):
    return HttpResponse(simplejson.dumps({'xxx': 'yyy'}),mimetype='application/json')
