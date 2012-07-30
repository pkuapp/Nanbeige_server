# -*- coding: utf-8 -*-

from django.http import HttpResponse
from django.utils import simplejson
from django.shortcuts import *
from django.conf import settings
from nbg.models import App
from nbg.helpers import json_response

@json_response
def version_api(request):
    return {'version':settings.API_VERSION}

@json_response
def version_android(request):
    app_obj = App.objects.all()[0]
    return {
        'stable': app_obj.version_android_stable,
        'beta': app_obj.version_android_beta
        }
        
@json_response
def version_ios(request):
    app_obj = App.objects.all()[0]
    return {
        'stable': app_obj.version_ios_stable,
        'beta': app_obj.version_ios_beta
        }

@json_response
def notice(request):
    app_obj = App.objects.all()[0]
    notice_time = str(app_obj.notice_time)
    return HttpResponse(simplejson.dumps({
        'time': notice_time,
        'content': app_obj.notice_content
        }), mimetype='application/json')
