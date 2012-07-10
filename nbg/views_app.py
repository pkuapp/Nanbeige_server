# -*- coding:UTF-8 -*-
from django.http import HttpResponse
from django.utils import simplejson

def version_api(request):
    return HttpResponse(simplejson.dumps({'version':'9'}), mimetype='application/json')

def version_android(request):
    return HttpResponse(simplejson.dumps({'stable':'0.618', 'beta':'0.619'}), mimetype='application/json')

def version_ios(request):
    return HttpResponse(simplejson.dumps({'stable':'1.0', 'beta':'1.1'}), mimetype='application/json')

def notice(request):
    return HttpResponse(simplejson.dumps({'time':'2012-04-01 00:00:00', 'content':'由于不可抗拒的因素，颐和园路5号将不再提供服务。'}), mimetype='application/json')