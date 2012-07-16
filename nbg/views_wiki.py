# -*- coding:UTF-8 -*-

from django.http import HttpResponse
from django.utils import simplejson

def wiki_list(request, university_id):
    return HttpResponse(simplejson.dumps([
        {'title': 'info of school bus', 'node_id': '111'},
        {'title': 'info of the campus', 'node_id': '222'}
    ]), mimetype='application/json')

def wiki_node(request):
    return HttpResponse(simplejson.dumps({'title':'info of school bus','type':'list','list':[{'title':'yu quanlu','node_id':'113'},{'title':'zi jin','node_id':'114'}]},{'title':'yu quanlu','type':'article','content':'drop at every 15 minutes'}),mimetype='application/json')
