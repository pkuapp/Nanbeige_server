# -*- coding:UTF-8 -*-
from django.http import HttpResponse
from django.utils import simplejson
from django.shortcuts import *
from nbg.models import *

def building_list(request):
    university_id = request.GET.get('university_id', None)
    building_array = Building.objects.filter(university=university_id).values()
    response = [ {'id' : item['id'], 'name': item['name'], 'latitude': float(item['latitude']), 'longitude': float(item['longitude']) } for item in building_array]
    return HttpResponse(simplejson.dumps(response,sort_keys=True),mimetype='application/json')

def room_list(request):
    return HttpResponse(simplejson.dumps([{'id':'101','name':'room 101','available':['true or false?']},{'id':'102','name':'room 102','available':['true or false?']},'...']),mimetype='application/json')