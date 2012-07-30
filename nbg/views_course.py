# -*- coding: utf-8 -*-

from django.http import HttpResponse
from django.utils import simplejson
from datetime import datetime
from nbg.models import Course, Assignment
from nbg.helpers import listify, json_response
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods

@json_response
def course_list(request):
    user = request.user
    course_objs = user.course_set.all()
    response = [{
        'id': item.pk,
        'orig_id': item.original_id,
        'name': item.name,
        'credit': float(item.credit),
        'teacher': [ teacher.name for teacher in item.teacher_set.all() ],
        'ta': [ ta.name for ta in item.ta_set.all() ],
        'semester_id': item.semester.pk,
        'week': listify(item.weeks),
        'lessons': [{
            'day': lesson.day,
            'start': lesson.start,
            'end': lesson.end,
            'location': lesson.location,
        } for lesson in item.lesson_set.all()]
    } for item in course_objs]
    return response

@json_response
def assignment_list(request):
    user = request.user
    assignment_objs = user.assignment_set.all()
    response = [{
        'id': item.pk,
        'course': item.course.name,
        'due': item.due.isoformat(' '),
        'content': item.content, 
        'finished': item.finished,
        'last_modified': item.last_modified.isoformat(' '),
    } for item in assignment_objs]
    return response

@json_response
def assignment_finish(request, offset):
    assignment_id = int(offset)
    assignment_finish = request.POST.get('finished', None)

    response = 0
    if assignment_finish:
        assignment_obj = Assignment.objects.filter(id=assignment_id)[0]
        assignment_obj.finished = assignment_finish
        assignment_obj.last_modified = datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S')
        assignment_obj.save()
    else:
        response = 'lack of POST parameter'
    return response

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

@json_response
def comment_list(request, offset):
    course_id = int(offset)
    start = request.GET.get('start', None)
    if not start:
        start = 0
    # else:
    #     start = int(start)

    comment_objs = Course.objects.get(pk=course_id).comment_set.all()[start : start + 10]

    response = [{
        'id': item.pk,
        'writer': item.writer.username,
        'time': item.time,
        'content': item.content,
    } for item in comment_objs]

    return response