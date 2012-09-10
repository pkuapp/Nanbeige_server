# -*- coding: utf-8 -*-

from django.views.decorators.http import require_http_methods
from datetime import datetime
from nbg.models import Course, Assignment, Comment, Semester, UserAction, CourseStatus
from nbg.helpers import listify_str, json_response, auth_required, parse_datetime, find_in_db, add_to_db, float_nullable
from spider.grabbers.grabber_base import LoginError, GrabError
from django.core.cache import cache
from django.http import HttpResponse

@auth_required
@json_response
def course_list(request):
    user = request.user
    course_statuses = (user.get_profile().coursestatus_set.all().
      select_related('course').prefetch_related('course__lesson_set'))
    response = [{
        'id': course_status.course_id,
        'status': CourseStatus.STATUS_CHOICES_DICT[course_status.status],
        'orig_id': course_status.course.original_id,
        'name': course_status.course.name,
        'credit': float_nullable(course_status.course.credit),
        'teacher': listify_str(course_status.course.teacher),
        'ta': listify_str(course_status.course.ta),
        'semester_id': course_status.course.semester_id,
        'lessons': [{
            'day': lesson.day,
            'start': lesson.start,
            'end': lesson.end,
            'location': lesson.location,
            'weekset_id': lesson.weekset_id,
        } for lesson in course_status.course.lesson_set.all()]
    } for course_status in course_statuses]

    return response

@json_response
def course(request, offset):
    course_id = int(offset)

    try:
        course = Course.objects.get(pk=course_id)
    except Course.DoesNotExist:
        return {'error_code': 'CourseNotFound'}

    response = {
        'id': course_id,
        'orig_id': course.original_id,
        'name': course.name,
        'credit': float(course.credit),
        'teacher': listify_str(course.teacher),
        'ta': listify_str(course.ta),
        'semester_id': course.semester_id,
        'lessons': [{
            'day': lesson.day,
            'start': lesson.start,
            'end': lesson.end,
            'location': lesson.location,
            'weekset_id': lesson.weekset_id,
        } for lesson in course.lesson_set.all()]
    }

    return response

@json_response
def all(request):
    semester_id = request.GET.get('semester_id', None)

    if not semester_id:
        return {'error_code': 'SyntaxError'}, 400
    try:
        semester = Semester.objects.get(pk=semester_id)
    except Semester.DoesNotExist:
        return {'error_code': 'SemesterNotFound'}, 404

    cache_name = 'semester_{0}_courses'.format(semester.pk)
    courses = cache.get(cache_name)
    if not courses:
        courses = semester.course_set.values("id", "name")
        # timeout: one week
        cache.set(cache_name, courses, 604800)
    return list(courses)

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
def assignment_modify(request, offset):
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
def edit(request, offset):
    course_id = int(offset)
    status = request.POST.get('status', None)

    try:
        course = Course.objects.get(pk=course_id)
    except Course.DoesNotExist:
        return {'error_code': 'CourseNotFound'}, 404

    if status not in ('select', 'audit', 'none'):
        return {'error_code': 'SyntaxError'}, 400

    user_profile = request.user.get_profile()

    if status == 'select' or status == 'audit':
        if status == 'select':
            status_value = CourseStatus.SELECT
        elif status == 'audit':
            status_value = CourseStatus.AUDIT

        try:
            course_status = CourseStatus.objects.get(user_profile=user_profile, course=course)
        except CourseStatus.DoesNotExist:
            CourseStatus.objects.create(user_profile=user_profile, course=course, status=status_value)
        else:
            course_status.status = status_value
            course_status.save()
    elif status == 'none':
        CourseStatus.objects.filter(user_profile=user_profile, course=course).delete()

    return 0

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

    Comment.objects.create(course=course, writer=request.user, time=datetime.now(), content=content)

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
            user_profile = request.user.get_profile()
            CourseStatus.objects.filter(user_profile=user_profile, status=CourseStatus.SELECT).delete()
            semester = Semester.objects.get(pk=grabber.semester_id)
            db_updated = False
            for c in grabber.courses:
                course = find_in_db(c)
                if not course:
                    course = add_to_db(c, semester)
                    db_updated = True
                CourseStatus.objects.create(user_profile=user_profile,
                  course=course, status=CourseStatus.SELECT)
            if db_updated:
                cache_name = 'semester_{0}_courses'.format(semester.pk)
                cache.delete(cache_name)
            UserAction.objects.create(user=request.user, semester=semester, action_type=UserAction.COURSE_IMPORTED)
            return {'semester_id': grabber.semester_id}
        except LoginError as e:
            if e.error == "auth":
                return {'error_code': 'AuthError'}
            elif e.error == "captcha":
                return {'error_code': 'CaptchaError'}
            else:
                return {'error_code': 'UnknownLoginError'}
        except GrabError as e:
            return {
                'error_code': 'GrabError',
                'error': e.error,
            }
    else:
        return {
            'error_code': 'GrabberExpired',
        }, 503

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
