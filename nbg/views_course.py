# -*- coding: utf-8 -*-

from django.views.decorators.http import require_http_methods
from datetime import datetime
from nbg.models import Course, Assignment, Comment, Lesson, Semester, UserAction
from nbg.helpers import listify_int, listify_str, json_response, auth_required, parse_datetime, find_in_db, add_to_db
from spider.grabbers.grabber_base import LoginError
from spider.grabbers.helpers import pretty_format
from django.core.cache import cache
from django.http import HttpResponse

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
        'teacher': listify_str(item.teacher),
        'ta': listify_str(item.ta),
        'semester_id': item.semester.pk,
        'lessons': [{
            'day': lesson.day,
            'start': lesson.start,
            'end': lesson.end,
            'location': lesson.location,
            'week': listify_int(lesson.weeks),
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
        return {'error': '作业不存在。'}, 404

    if assignment.user != request.user:
        return {'error': '作业不属于当前用户。'}, 403

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
        return {'error': '作业不存在。'}, 404

    if assignment.user != request.user:
        return {'error': '作业不属于当前用户。'}, 403

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
        return {'error': '作业不存在。'}, 404

    if assignment.user != request.user:
        return {'error': '作业不属于当前用户。'}, 403

    course_id = request.POST.get('course_id', None)
    due = request.POST.get('due', None)
    content = request.POST.get('content', None)
    finished = request.POST.get('finished', None)

    if course_id:
        try:
            course = Course.objects.get(pk=course_id)
        except Course.DoesNotExist:
            return {'error': '课程不存在。'}, 404
        try:
            request.user.get_profile().courses.get(pk=course_id)
        except Course.DoesNotExist:
            return {'error': '课程不属于当前用户。'}, 403
        assignment.course = course
    if due:
        try:
            assignment.due = parse_datetime(due)
        except ValueError:
            return {'error': '截止日期格式错误。'}, 400
    if content:
        assignment.content = content
    if finished:
        assignment.finished = finished

    assignment.last_modified = datetime.now()
    assignment.save()

    return 0

@require_http_methods(['POST'])
@auth_required
@json_response
def assignment_add(request):
    course_id = request.POST.get('course_id', None)
    due = request.POST.get('due', None)
    content = request.POST.get('content', None)

    if course_id and due and content:
        try:
            course = Course.objects.get(pk=course_id)
        except Course.DoesNotExist:
            return {'error': '课程不存在。'}, 404
        try:
            request.user.get_profile().courses.get(pk=course_id)
        except Course.DoesNotExist:
            return {'error': '课程不属于当前用户。'}, 403

        try:
            due = parse_datetime(due)
        except ValueError:
            return {'error': '截止日期格式错误。'}, 400

        assignment = Assignment(course=course, user=request.user, due=due, content=content,
          finished=False, last_modified=datetime.now())
        assignment.save()
        return {'id': assignment.pk}
    else:
        return {'error': '缺少必要的参数。'}, 400

@require_http_methods(['POST'])
@auth_required
@json_response
def comment_add(request, offset):
    course_id = int(offset)
    content = request.POST.get('content', None)

    if not content:
        return {'error': '缺少必要的参数。'}, 400
    try:
        course = Course.objects.get(pk=course_id)
    except Course.DoesNotExist:
        return {'error': '课程不存在。'}, 404
    try:
        request.user.get_profile().courses.get(pk=course_id)
    except Course.DoesNotExist:
        return {'error': '课程不属于当前用户。'}, 403

    comment = Comment(course=course, writer=request.user, time=datetime.now(), content=content)
    comment.save()

    return 0

@json_response
def comment_list(request, offset):
    course_id = int(offset)
    start = int(request.GET.get('start', 0))

    try:
        course = Course.objects.get(pk=course_id)
    except Course.DoesNotExist:
        return {'error': '课程不存在。'}, 404

    comment_objs = course.comment_set.all()[start:start+10]

    response = [{
        'id': item.pk,
        'writer': item.writer.username,
        'time': item.time.isoformat(' '),
        'content': item.content,
    } for item in comment_objs]

    return response

@require_http_methods(['POST'])
@auth_required
@json_response
def course_grab(request):
    user = request.user
    university = user.get_profile().campus.university
    try:
        exec("from spider.grabbers import grabber_" + str(int(university.pk)) + " as GrabberModel")
    except ImportError:
        return {'available': False}
    grabber = GrabberModel.TeapotParser()

    response = grabber.work_flow_type()

    cache.set(request.session.session_key+'_grabber', grabber)

    return response

@require_http_methods(['POST'])
@auth_required
@json_response
def course_grab_start(request):
    grabber = cache.get(request.session.session_key+'_grabber')
    if grabber:
        try:
            grabber.setUp(**request.POST.dict())
        except LookupError:
            return {'error_code': 'SyntaxError'}, 400

        try:
            grabber.run()
            semester = Semester.objects.get(pk=grabber.semester_id)
            for c in grabber.courses:
                course = find_in_db(c)
                if course:
                    request.user.get_profile().courses.add(course)
                else:
                    course = add_to_db(c, semester)
                    request.user.get_profile().courses.add(course)
            UserAction.objects.create(user=request.user, semester=semester, action_type=UserAction.COURSE_IMPORTED)
            return {'semester_id': grabber.semester_id}
        except LoginError as e:
            if e.error == "auth":
                return {'error_code': 'AuthError'}
            elif e.error == "captcha":
                return {'error_code': 'CaptchaError'}
            else:
                return {'error_code': 'UnknownLoginError'}
    else:
        return {'error': '导入课程无法启动或抓取器已过期。'}, 503

@require_http_methods(['GET'])
@auth_required
def captcha_img(request):
    grabber = cache.get(request.session.session_key+'_grabber')
    if grabber and grabber.captcha_img:
        return HttpResponse(grabber.captcha_img, mimetype="image")
    else:
        return json_response(lambda x:({
            'error': '验证码不存在或已过期。'
        }, 404))()
