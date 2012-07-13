# -*- coding:UTF-8 -*-
from django.shortcuts import *
from django.template import RequestContext
from django.http import HttpResponse

from nbg.models import *
from django.contrib import auth
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.utils import simplejson
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from datetime import datetime

def query(request):
    keyword =request.GET.get('keyword', None)
    category = request.GET.get('category'. None)
    after = request.GET.get('after', None)
    before = request.GET.get('before',None)
    start = request.GET.get('start', None)
    batch = request.GET.get('batch', None)

    event_objs = Event.objects.all()
    if keyword:
        event_objs = event_objs.filter(titel = keyword())
    if category_id:
        event_objs = event_objs.filter(category_id = category_id())
    if after:
        event_objs = event_objs.filter(time_gte = datetime.fromtimestamp(float(after)))
    else:
        event_objs = event_objs.filter(time_gte = datetime.now())
    if before:
        event_objs = event_objs.filter(time_lte = datetime.fromtimestamp(float(before)))
    if not start:
        start = 0
    if not batch:
        batch =10
    event_objs = event_objs[int(start):int(batch)]
def address(request):
    return HttpResponse(simplejson.dumps({'event':'???'}),mimetype='application/json')