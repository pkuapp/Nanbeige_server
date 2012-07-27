# -*- coding: utf-8 -*-

from django.http import HttpResponse, HttpResponseNotFound
from django.utils import simplejson
from datetime import time
from nbg.models import University
from nbg.helpers import listify

def university_list(request):
    universities = University.objects.all()
    response = [{
        'id': university.pk,
        'name': university.name,
        'location': {
            'latitude': float(university.latitude),
            'longitude': float(university.longitude)
        }
    } for university in universities]
    return HttpResponse(simplejson.dumps(response), mimetype='application/json')

def detail(request, offset):
    university_id = int(offset)
    try:
        university = University.objects.get(pk=university_id)
    except:
        response = {
            'error': "学校不存在。",
        }
        return HttpResponseNotFound(simplejson.dumps(response), mimetype='application/json')

    schedule_unit = university.scheduleunit_set.all()

    lessons_total = university.lessons_morning + university.lessons_afternoon + university.lessons_evening
    response = {
        'name': university.name,
        'location': {
            'latitude': float(university.latitude),
            'longitude': float(university.longitude),
        },
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
            'separators': listify(university.lessons_separator)
        }
    }
    return HttpResponse(simplejson.dumps(response), mimetype='application/json')

def semester(request, offset):
    university_id = int(offset)
    university = University.objects.get(pk=university_id)
    
    semesters = university.semester_set.all()
    
    response = [{
        'id': semester.pk,
        'name': semester.name,
        'week': {
            'start': semester.week_start.isoformat(),
            'end': semester.week_end.isoformat(),
            'excluded': listify(semester.excluded)
        }
    } for semester in semesters]
    return HttpResponse(simplejson.dumps(response), mimetype='application/json')
