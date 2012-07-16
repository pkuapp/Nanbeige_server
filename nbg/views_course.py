# -*- coding:UTF-8 -*-
from django.http import HttpResponse
from django.utils import simplejson
from nbg.models import *
from datetime import datetime
from datetime import time

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
    #course_id = int(offset)
  #  if course_id:
    #    pdate = datetime.strptime(request.GET.get('date' ,None), %Y-%m-%d %H-%M-%S)
  #      assignment_values = Assignment.objects.filter(course = course_id).values()
    assignment_values = Assignment.objects.all()
    response = [{
        'id' : item.id,
        'course' : item.course.name,
        'due' : datetime.strftime(item.due, '%Y-%m-%D %H:%M:%S'),
        'content' : item.content, 
        'finished' : Assignment.objects.filter(course = item.id).values()[0]['finished'],
        'last_modified' : datetime.strftime(item.last_modified, '%Y-%m-%D %H:%M:%S'),
    } for item in assignment_values]
    return HttpResponse(simplejson.dumps(response),mimetype='application/json')
