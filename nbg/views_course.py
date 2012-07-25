# -*- coding: utf-8 -*-

from django.http import HttpResponse
from django.utils import simplejson
from datetime import datetime
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

#waiting for testing!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
#@login_required
#@require_http_methods(['POST' ,])
def assignment_finish(request, offset):
    assignment_id = int(offset)
    assignment_finish = request.POST.get('finished', None)
    if assignment_finish:
        assignment_obj = Assignment.objects.filter(id=assignment_id)[0]
        assignment_obj.finished = assignment_finish
        assignment_obj.last_modified = datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S')
        assignment_obj.save()
        return HttpResponse(0)
    else:
        return HttpResponse(simplejson.dumps('lack of POST parameter'),mimetype ='application/json')

def assignment_delete(request, offset):
    assignment_id = int(offset)
    assignment_obj = Assignment.objects.filter(id=assignment_id)[0]
    assignment_obj.delete()
    return HttpResponse(0)

def assignment_modify(request,offset):
    assignment_id = int(offset)
    assignment_finish = request.POST.get('finished', None)
    assignment_due = request.POST.get('due', None)
    assignment_content = request.POST.get('content', None)
    assignment_courseid = request.POST.get('course_id', None)
    
    assignment_obj = Assignment.objects.filter(id=assignment_id)[0]
    assignment_obj.finished = assignment_finish
    assignment_obj.last_modified = datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S')
    assignment_obj.due = datetime.strftime(assignment_due, '%Y-%m-%d %H:%M:%S')  
    assignment_obj.content = assignment_content
    assignment_obj.course_id = assignment_courseid
    assignment_obj.save()
    return HttpResponse(0)

def assignment_add(request):
    assignment_courseid = request.POST.get('course_id', None)
    assignment_due = request.POST.get('due', None)
    assignment_content = request.POST.get('content', None)
    assignment_obj = Course(course_id=assignment_courseid, due=datetime.strftime(assignment_due, '%Y-%m-%d %H:%M:%S', content=assignment_content))
    assignment_obj.save()
    return HttpResponse(0)

def comment_add(request, offset):
    comment_id = int(offset)
    comment_content = request.POST.get('content', None)
    comment_obj = Course(id=course_id, content=comment_content)
    comment_obj.save()
    return HttpResponse(0)

def comment_list(request, offset):
    start = int(request.GET.get('start', None))
    if course_id:
        course_objs =Comment.objects.filter(course_id = int(offset))  
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
