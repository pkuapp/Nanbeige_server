# -*- coding:UTF-8 -*-
from django.http import HttpResponse
from django.utils import simplejson
from django.shortcuts import *
from nbg.models import *
from datetime import datetime

def building_list(request):
    university_id = request.GET.get('university_id', None)
    if university_id:
        try:
            building_values = Building.objects.filter(university=university_id).values()
            response = [ {'id' : item['id'], 'name': item['name'], 'latitude': float(item['latitude']), 'longitude': float(item['longitude']) } for item in building_values]
            return HttpResponse(simplejson.dumps(response,sort_keys=True),mimetype='application/json')
        except:
            return HttpResponse(simplejson.dumps({'error': '尚无数据'}),mimetype='application/json')
    else:
        return HttpResponse(simplejson.dumps({'error': '缺少必要的参数'}),mimetype='application/json')

def room_list(request, offset):
    building_id = int(offset)
    if building_id and request.GET.get('date', None):
        pdate = datetime.strptime(request.GET.get('date', None), '%Y%m%d')
        try:
            room_values = Classroom.objects.filter(building=building_id).values()
            response = [ {'id' : item['id'], 'name': item['name'], 'availability': ClassroomAvailability.objects.filter(classroom=item['id'], date=pdate).values()[0]['availability']} for item in room_values]
            return HttpResponse(simplejson.dumps(response,sort_keys=True),mimetype='application/json')
        except:
            return HttpResponse(simplejson.dumps({'error': '尚无数据'}),mimetype='application/json')
    else:
        return HttpResponse(simplejson.dumps({'error': '缺少必要的参数'}),mimetype='application/json')
