# -*- coding:UTF-8 -*-
from django.http import HttpResponse
from django.utils import simplejson
from nbg.models import *


def course_list(request):
    course_values = Course.objects.all()
    response = [{
        'id' : item.pk,
        'orig_id' : item.original_id,
        'name' : item.name,
        'credit' : float(item.credit),
        'teacher' : [ teacher.name for teacher in item.teacher_set.all() ],
        'ta' : [ ta.name for ta in item.ta_set.all() ],
        'week' : item.weeks,
        'lessons': [{
            'day': lesson.day,
            'start' : lesson.start,
            'end' : lesson.end,
            'location' : lesson.location,
        } for lesson in item.lesson_set.all()]
    } for item in course_values]
    return HttpResponse(simplejson.dumps(response), mimetype='application/json')

def assignment_list(request):
    return HttpResponse(simplejson.dumps({'xxx': 'yyy'}),mimetype='application/json')
