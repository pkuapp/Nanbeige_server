# -*- coding: utf-8 -*-

from string import split
from datetime import datetime
from json import dumps
from django.http import HttpResponse

def listify_str(str):
    ret_list = split(str, ',')
    if ret_list[0] == "":
        ret_list = []
    return ret_list

def listify_int(str):
    return map(int, listify_str(str))

def parse_datetime(str):
    return datetime.strptime(str, "%Y-%m-%d %H:%M:%S")

def json_response(func):
    def inner(request=None, *args, **kwargs):
        status_code = 200
        response = func(request, *args, **kwargs)
        content = response
        if isinstance(response, tuple):
            content = response[0]
            status_code = response[1]
        return HttpResponse(dumps(content, ensure_ascii=False, separators=(',',':')),
          mimetype="application/json", status=status_code)

    return inner

def auth_required(func):
    def inner(request, *args, **kwargs):
        if request.user.is_authenticated():
            return func(request, *args, **kwargs)
        else:
            return HttpResponse(dumps({'error_code': 'NotLoggedIn'}), mimetype="application/json", status=403)
    return inner
