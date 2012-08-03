# -*- coding: utf-8 -*-

from datetime import time
from nbg.models import University
from nbg.helpers import listify_int
from nbg.helpers import json_response

@json_response
def university_list(request):
    universities = University.objects.all()
    response = [{
        'id': university.pk,
        'name': university.name,
    } for university in universities]
    return response

@json_response
def detail(request, offset):
    university_id = int(offset)
    try:
        university = University.objects.get(pk=university_id)
    except University.DoesNotExist:
        return {'error': "学校不存在。"}, 404

    schedule_unit = university.scheduleunit_set.all()

    lessons_total = university.lessons_morning + university.lessons_afternoon + university.lessons_evening
    response = {
        'name': university.name,
        'campuses': [{
            'name': campus.name,
            'location': {
                'latitude': float(campus.latitude),
                'longitude': float(campus.longitude),
            }
        } for campus in university.campus_set.all()],
        'support': {
            'import_course': university.support_import_course,
            'list_course': university.support_list_course,
        },
        'lessons': {
            'count': {
                'total': lessons_total,
                'morning': university.lessons_morning,
                'afternoon': university.lessons_afternoon,
                'evening': university.lessons_evening,
            },
            'detail': [{
                'number': item.number,
                'start': time.strftime(item.start, "%H:%M"),
                'end': time.strftime(item.end, "%H:%M"),
            } for item in schedule_unit],
            'separators': listify_int(university.lessons_separator)
        }
    }
    return response

@json_response
def semester(request, offset):
    university_id = int(offset)
    university = University.objects.get(pk=university_id)

    semesters = university.semester_set.all()

    response = [{
        'id': semester.pk,
        'name': semester.name,
        'year': semester.year,
        'week': {
            'start': semester.week_start.isoformat(),
            'end': semester.week_end.isoformat(),
            'excluded': listify_int(semester.excluded)
        }
    } for semester in semesters]
    return response
