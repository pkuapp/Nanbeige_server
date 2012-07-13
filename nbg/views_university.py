# -*- coding:UTF-8 -*-

from django.http import HttpResponse
from django.utils import simplejson
from nbg.models import *
from datetime import datetime
from datetime import time
from string import split

def university_list(request):
    try:
        university_values = University.objects.values()
        response = [{'id': item['id'], 'name': item['name'], 'location': {'latitude': float(item['latitude']), 'longitude': float(item['longitude'])}} for item in university_values]
        return HttpResponse(simplejson.dumps(response, sort_keys=True), mimetype = 'application/json')
    except:
        return HttpResponse(simplejson.dumps({'error': '尚无数据'}), mimetype='application/json')

def detail(request, offset):
    university_id = int(offset)
    if university_id:
        try:
            university_detail = University.objects.get(pk=university_id)
            schedule_unit = ScheduleUnit.objects.filter(university_id=university_id).values()
            excluded = split(university_detail.excluded, ',')
            if excluded[0] == "":
                excluded = []
            else:
                excluded = map(int, excluded)
                lessons_total = university_detail.lessons_morning + university_detail.lessons_afternoon + university_detail.lessons_evening
                response = {
                'name': university_detail.name,
                'location': {
                    'latitude': float(university_detail.latitude),
                    'longitude': float(university_detail.longitude)},
                'support': {
                    'import_course': university_detail.support_import_course,
                    'list_course': university_detail.support_list_course},
                'week': {
                    'start': datetime.strftime(university_detail.week_start , '%Y-%m-%d'),
                    'end': datetime.strftime(university_detail.week_end, '%Y-%m-%d'),
                    'excluded': excluded,},
                'lessons': {
                    'count': {
                        'total': lessons_total,
                        'morning': university_detail.lessons_morning,
                        'afternoon': university_detail.lessons_afternoon,
                        'evening': university_detail.lessons_evening,},
                    'detail': [
                    {
                        'number': item['number'],
                        'start': time.strftime(item['start'], "%H:%M"),
                        'end': time.strftime(item['end'], "%H:%M"),
                    } for item in schedule_unit]
                }
                }
            return HttpResponse(simplejson.dumps(response), mimetype = 'application/json')
        except:
            raise
        else:
            pass
        finally:
            pass
    else:
        return HttpResponse("haha")

