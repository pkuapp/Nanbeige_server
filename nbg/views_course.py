# -*- coding: utf-8 -*-

from django.http import HttpResponse
from django.views.decorators.http import require_http_methods
from datetime import datetime
import dateutil.parser
from nbg.models import Course, Assignment
from nbg.helpers import listify, json_response, auth_required

@auth_required
@json_response
def course_list(request):
    user = request.user
    course_objs = user.get_profile().courses.all()
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

@auth_required
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

@require_http_methods(['POST'])
@auth_required
@json_response
def assignment_finish(request, offset):
    id = int(offset)
    finished = int(request.POST.get('finished', 1))

    try:
        assignment = Assignment.objects.get(pk=id)
    except Assignment.DoesNotExist:
        return {'error': '作业不存在。'}

    if assignment.user != request.user:
        return {'error': '作业不属于当前用户。'}

    assignment.finished = finished
    assignment.last_modified = datetime.now()
    assignment.save()

    return 0

@require_http_methods(['POST'])
@auth_required
@json_response
def assignment_delete(request, offset):
    id = int(offset)

    try:
        assignment = Assignment.objects.get(pk=id)
    except Assignment.DoesNotExist:
        return {'error': '作业不存在。'}

    if assignment.user != request.user:
        return {'error': '作业不属于当前用户。'}

    assignment.delete()

    return 0

@require_http_methods(['POST'])
@auth_required
@json_response
def assignment_modify(request,offset):
    id = int(offset)

    try:
        assignment = Assignment.objects.get(pk=id)
    except Assignment.DoesNotExist:
        return {'error': '作业不存在。'}

    if assignment.user != request.user:
        return {'error': '作业不属于当前用户。'}

    course_id = request.POST.get('course_id', None)
    due = request.POST.get('due', None)
    content = request.POST.get('content', None)
    finished = request.POST.get('finished', None)

    if course_id:
        try:
            course = Course.objects.get(pk=course_id)
        except Course.DoesNotExist:
            return {'error': '课程不存在。'}
        try:
            request.user.get_profile().courses.get(pk=course_id)
        except Course.DoesNotExist:
            return {'error': '课程不属于当前用户。'}
        assignment.course = course
    if due:
        try:
            assignment.due = dateutil.parser.parse(due)
        except ValueError:
            return {'error': '截止日期格式错误。'}
    if content:
        assignment.content = content
    if finished:
        assignment.finished = finished

    assignment.last_modified = datetime.now()
    assignment.save()

    return 0

@require_http_methods(['POST'])
@auth_required
def assignment_add(request):
    assignment_courseid = request.POST.get('course_id', None)
    assignment_due = request.POST.get('due', None)
    assignment_content = request.POST.get('content', None)
    assignment_obj = Course(course_id=assignment_courseid, due=datetime.strftime(assignment_due, '%Y-%m-%d %H:%M:%S', content=assignment_content))
    assignment_obj.save()
    return HttpResponse(0)

@require_http_methods(['POST'])
@auth_required
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
