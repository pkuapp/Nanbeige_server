# -*- coding: utf-8 -*-

from django.http import HttpResponse, HttpResponseNotFound
from django.utils import simplejson
from datetime import datetime, time
from nbg.models import *
from nbg.helpers import listify

def university_list(request):
    university_values = University.objects.values()
    response = [{
        'id': item['id'],
        'name': item['name'],
        'location': {
            'latitude': float(item['latitude']),
            'longitude': float(item['longitude'])
        }
    } for item in university_values]
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

    excluded = listify(university.excluded)

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
        'week': {
            'start': datetime.strftime(university.week_start, '%Y-%m-%d'),
            'end': datetime.strftime(university.week_end, '%Y-%m-%d'),
            'excluded': excluded,
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
