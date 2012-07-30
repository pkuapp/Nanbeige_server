# -*- coding: utf-8 -*-

from django.http import HttpResponse, HttpResponseNotFound
from django.utils import simplejson
from datetime import date as datetime_date
from nbg.models import University, Building, RoomAvailability
from nbg.helpers import listify,json_response

@json_response
def building_list(request):
    university_id = int(request.GET.get('university_id', 0))

    try:
        university = University.objects.get(pk=university_id)
    except:
        return {'error': '学校不存在。'}

    buildings = university.building_set.all()
    response = [{
        'id': building.id,
        'name': building.name,
        'location': {
            'latitude': float(building.latitude),
            'longitude': float(building.longitude),
        },
    } for building in buildings]
    return response

@json_response
def room_list(request, offset):
    building_id = int(offset)
    date = request.GET.get('date', datetime_date.today())

    try:
        building = Building.objects.get(pk=building_id)
    except Building.DoesNotExist:
        return {'error': '教学楼不存在。'}

    room_objs = building.room_set.all()
    response = []
    for room in room_objs:
        try:
            availability = listify(room.roomavailability_set.get(date=date).availability)
        except RoomAvailability.DoesNotExist:
            availability = []

        item = {
            'id': room.id,
            'name': room.name,
            'availability': availability,
        }
        response.append(item)
    return response

