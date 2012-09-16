# -*- coding: utf-8 -*-

from string import split
from datetime import datetime
from json import dumps
import re
from django.http import HttpResponse
from django.db import connection
from django.conf import settings
from nbg.models import Course, Lesson

def unify_brackets(text):
    return re.sub(u'\((.{0,10})）', lambda(obj):u'（{0}）'.format(obj.group(1)), text)

def float_nullable(number):
    if number is None:
        return None
    return float(number)

def listify_str(str):
    ret_list = split(str, ',')
    if ret_list[0] == "":
        ret_list = []
    return ret_list

def listify_int(str):
    return map(int, listify_str(str))

def parse_datetime(str):
    return datetime.strptime(str, "%Y-%m-%d %H:%M:%S")

def once_upon_a_time():
    return datetime(2000, 1, 1, 0, 0)

def json_response(func):
    def inner(request=None, *args, **kwargs):
        status_code = 200
        response = func(request, *args, **kwargs)
        content = response
        if isinstance(response, tuple):
            content = response[0]
            status_code = response[1]
        if settings.DEBUG:
            return HttpResponse(dumps(content, ensure_ascii=False, indent=2),
              mimetype="application/json", status=status_code)
        else:
            return HttpResponse(dumps(content, ensure_ascii=False, separators=(',',':')),
              mimetype="application/json", status=status_code)

    return inner

def append_query(func):
    def inner(request=None, *args, **kwargs):
        response = func(request, *args, **kwargs)
        if isinstance(response, dict):
            response.update({
                'queries': connection.queries,
                'queries_count': len(connection.queries),
            })
        elif isinstance(response, list):
            response.append(connection.queries)
            response.append(len(connection.queries))
        return response
    return inner

def auth_required(func):
    def inner(request, *args, **kwargs):
        if request.user.is_authenticated():
            return func(request, *args, **kwargs)
        else:
            return HttpResponse(dumps({'error_code': 'NotLoggedIn'}), mimetype="application/json", status=403)
    return inner

def is_same(lesson_set, lessons):
    if lesson_set.count() != len(lessons):
        return False
    for l in lessons:
        if not lesson_set.filter(**l).exists():
            return False
    return True

def find_in_db(c):
    c = c.copy()
    lessons = c.pop('lessons')
    similar_courses = Course.objects.filter(**c)
    for course in similar_courses:
        if is_same(course.lesson_set, lessons):
            return course
    return None

def add_to_db(c, semester):
    """add a course to database"""
    c = c.copy()
    lessons = c.pop('lessons')
    course = Course.objects.create(semester=semester, **c)
    for l in lessons:
        if l:
            Lesson.objects.create(course=course, **l)
    return course
