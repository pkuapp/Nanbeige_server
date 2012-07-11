# -*- coding:UTF-8 -*-
from django.http import HttpResponse
from django.utils import simplejson

def building_list(request):
    return HttpResponse(simplejson.dumps([{'id':'xxx','name':'building 1'},{'id':'yyy','name':'building 2'}]),mimetype='application/json')

def room_list(request):
    return HttpResponse(simplejson.dumps([{'id':'101','name':'room 101','available':['true or false?']},{'id':'102','name':'room 102','available':['true or false?']},'...']),mimetype='application/json')