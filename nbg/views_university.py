# -*- coding: utf-8 -*-

from datetime import time
from nbg.models import University, Semester
from nbg.helpers import listify_int, json_response

@json_response
def university_list(request):
    universities = University.objects.all().prefetch_related('campus_set')
    response = [{
        'id': university.pk,
        'name': university.name,
        'campuses': [{
            'id': campus.pk,
            'name': campus.name,
        } for campus in university.campus_set.all()],
    } for university in universities]
    return response

@json_response
def detail(request, offset):
    university_id = int(offset)
    try:
        university = University.objects.get(pk=university_id)
    except University.DoesNotExist:
        return {'error_code': 'UniversityNotFound'}, 404

    schedule_unit = university.scheduleunit_set.all()

    response = {
        'name': university.name,
        'support': {
            'import_course': university.support_import_course,
            'list_course': university.support_list_course,
            'ta': university.support_ta,
        },
        'lessons': {
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
    try:
        university = University.objects.get(pk=university_id)
    except University.DoesNotExist:
        return {'error_code': "UniversityNotFound"}, 404

    semesters = university.semester_set.all()

    response = [{
        'id': semester.pk,
        'name': semester.name,
        'year': semester.year,
        'week': {
            'start': semester.week_start.isoformat(),
            'end': semester.week_end.isoformat()
        },
    } for semester in semesters]
    return response

@json_response
def weekset(request, offset):
    semester_id = int(offset)
    try:
        semester = Semester.objects.get(pk=semester_id)
    except Semester.DoesNotExist:
        return {'error_code': "SemesterNotFound"}, 404

    weeksets = semester.weekset_set.all()

    response = [{
        'id': weekset.pk,
        'name': weekset.name,
        'weeks': listify_int(weekset.weeks),
    } for weekset in weeksets]
    return response
