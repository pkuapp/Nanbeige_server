# -*- coding:UTF-8 -*-
from django.http import HttpResponse
from django.utils import simplejson
from datetime import datetime
from datetime import time
from nbg.models import *
from nbg.helpers import listify
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods

def course_list(request):
    course_values = Course.objects.all()
    response = [{
        'id' : item.pk,
        'orig_id' : item.original_id,
        'name' : item.name,
        'credit' : float(item.credit),
        'teacher' : [ teacher.name for teacher in item.teacher_set.all() ],
        'ta' : [ ta.name for ta in item.ta_set.all() ],
        'week' : listify(item.weeks),
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
        'due' : datetime.strftime(item.due, '%Y-%m-%d %H:%M:%S'),
        'content' : item.content, 
        'finished' : Assignment.objects.filter(course = item.id).values()[0]['finished'],
        'last_modified' : datetime.strftime(item.last_modified, '%Y-%m-%d %H:%M:%S'),
    } for item in assignment_values]
    return HttpResponse(simplejson.dumps(response),mimetype='application/json')

#@login_required
#@require_http_methods(['POST' ,])
def assignment_finish(request, offset):
    assignment_id = int(offset)
    assignment_finish = request.POST.get('finished', None)
    assignment_obj = Assignment.objects.filter(id = assignment_id)[0]
    assignment_obj.finished = assignment_finish
    assignment_obj.last_modified = datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S')
    response = assignment_obj.save()
    return HttpResponse(simplejson.dumps(response),mimetype ='application/json')





