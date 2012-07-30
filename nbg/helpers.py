# -*- coding: utf-8 -*-

from string import split
from django.utils.simplejson import dumps
from django.http import HttpResponse

def listify(str):
    ret_list = split(str, ',')
    if ret_list[0] == "":
        ret_list = []
    else:
        ret_list = map(int, ret_list)

    return ret_list

def json_response(func):
    def inner(request, *args, **kwargs):
        dict_response = func(request, *args, **kwargs)
        return HttpResponse(dumps(dict_response), mimetype="application/json")
    return inner

def auth_required(func):
    def inner(request, *args, **kwargs):
        if request.user.is_authenticated():
            return func(request, *args, **kwargs)
        else:
            return HttpResponse(dumps({'error': '请先登录。'}))
    return inner
