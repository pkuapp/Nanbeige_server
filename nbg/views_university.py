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
        response = [{
            'id': item['id'],
            'name': item['name'],
            'location': {
                'latitude': float(item['latitude']),
                'longitude': float(item['longitude'])
            }
        } for item in university_values]
        return HttpResponse(simplejson.dumps(response), mimetype='application/json')
    except:
        return HttpResponse(simplejson.dumps({'error': '尚无数据'}), mimetype='application/json')

def detail(request, offset):
    university_id = int(offset)
    if university_id:
        try:
            university = University.objects.get(pk=university_id)
            schedule_unit = university.scheduleunit_set.values()
            
            excluded = split(university.excluded, ',')
            if excluded[0] == "":
                excluded = []
            else:
                excluded = map(int, excluded)
            
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
                    'start': datetime.strftime(university.week_start , '%Y-%m-%d'),
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
<<<<<<< HEAD

=======
>>>>>>> 754f8906cde59f6ea6324529ab8554b7639872ba
