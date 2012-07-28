# -*- coding: utf-8 -*-

from django.http import HttpResponse, HttpResponseNotFound, HttpResponseBadRequest
from django.utils import simplejson
from django.shortcuts import *
from nbg.models import *
from nbg.helpers import listify
from datetime import datetime

def building_list(request):
    university_id = int(request.GET.get('university_id', 0))

    try:
        university = University.objects.get(pk=university_id)
    except:
        return HttpResponseNotFound(simplejson.dumps({'error': '学校不存在。'}), mimetype='application/json')

    buildings = university.building_set.all()
    response = [{
        'id': building.id,
        'name': building.name,
        'location': {
            'latitude': float(building.latitude),
            'longitude': float(building.longitude),
        },
    } for building in buildings]
    return HttpResponse(simplejson.dumps(response), mimetype='application/json')

def room_list(request, offset):
    building_id = int(offset)
    date = request.GET.get('date', None)
    if building_id and date:
        date = datetime.strptime(date, '%Y-%m-%d')
        try:
            building = Building.objects.get(pk=building_id)
            room_objs = building.room_set.all()
            response = [{
                'id': room.id,
                'name': room.name,
                'availability': listify(room.roomavailability_set.get(date=date).availability),
            } for room in room_objs]
            return HttpResponse(simplejson.dumps(response), mimetype='application/json')
        except:
            return HttpResponseNotFound(simplejson.dumps({'error': '教学楼不存在。'}), mimetype='application/json')    
    else:
        return HttpResponseBadRequest(simplejson.dumps({'error': '缺少必要的参数。'}), mimetype='application/json')
