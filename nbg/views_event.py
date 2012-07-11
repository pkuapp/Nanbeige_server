  # -*- coding:UTF-8 -*-
from django.http import HttpResponse
from django.utils import simplejson


def address(request):
    return HttpResponse(simplejson.dumps({'event':'???'}),mimetype='application/json')