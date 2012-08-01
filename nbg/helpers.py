# -*- coding: utf-8 -*-

from string import split
from datetime import datetime
from django.utils.simplejson import dumps
from django.http import HttpResponse
from django.core.cache import cache
from django.core.paginator import Paginator, Page

def listify(str):
    ret_list = split(str, ',')
    if ret_list[0] == "":
        ret_list = []
    else:
        ret_list = map(int, ret_list)

    return ret_list

def parse_datetime(str):
    return datetime.strptime(str, "%Y-%m-%d %H:%M:%S")

def json_response(func):
    def inner(request, *args, **kwargs):
        status_code = 200
        response = func(request, *args, **kwargs)
        content = response
        if isinstance(response, tuple):
            content = response[0]
            status_code = response[1]

        return HttpResponse(dumps(content),
          mimetype="application/json", status=status_code)

    return inner

def auth_required(func):
    def inner(request, *args, **kwargs):
        if request.user.is_authenticated():
            return func(request, *args, **kwargs)
        else:
            return HttpResponse(dumps({'error': '请先登录。'}), status=401)
    return inner