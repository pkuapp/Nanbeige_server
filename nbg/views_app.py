# -*- coding:UTF-8 -*-

from django.http import HttpResponse
from django.utils import simplejson
from django.shortcuts import *
from django.conf import settings
from datetime import datetime
from nbg.models import App

def version_api(request):
    return HttpResponse(simplejson.dumps({'version':settings.API_VERSION}), mimetype='application/json')

def version_android(request):
    app_obj = App.objects.all()[0]
    return HttpResponse(simplejson.dumps({
        'stable': app_obj.version_android_stable,
        'beta': app_obj.version_android_beta
        }), mimetype='application/json')

def version_ios(request):
    app_obj = App.objects.all()[0]
    return HttpResponse(simplejson.dumps({
        'stable': app_obj.version_ios_stable,
        'beta': app_obj.version_ios_beta
        }), mimetype='application/json')

def notice(request):
    app_obj = App.objects.all()[0]
    notice_time = str(app_obj.notice_time)
    return HttpResponse(simplejson.dumps({
        'time': notice_time,
        'content': app_obj.notice_content
        }), mimetype='application/json')
