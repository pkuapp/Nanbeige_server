# -*- coding: utf-8 -*-

from django.http import HttpResponse, HttpResponseNotFound
from django.utils import simplejson
from nbg.models import *
from datetime import datetime

def wiki_node(request, offset):
    node_id = int(offset)
    wikinode_obj = WikiNode.objects.get(pk=node_id)
    node_type = wikinode_obj.type
    if node_type == 'L':
        response = [{
            'title': listitem.title,
            'type': listitem.node_type,
            'father': listitem.father,
            'list': [{
                'title': typelist.title,
                'node_id': typelist.pk,
            } for typelist in typelist.list_set.all()]
        } for listitem in wikinode_obj]
    if node_type == 'A':
        response = {
            'title': wikinode_obj.title,
            'type': wikinode_obj.type,
            'content': wikinode_obj.content,
        }
    return HttpResponse(simplejson.dumps(response), mimetype='application/json')

def wiki_list(request, offset):
    university_id = int(offset)
    
    try:
        university_obj = University.objects.get(pk=university_id)
    except:
        response = {
            'error': "学校不存在。",
        }
        return HttpResponseNotFound(simplejson.dumps(response), mimetype='application/json')

    response = [{
        'title': item.node.title,
        'node_id': item.node.pk,
    } for item in university_obj.wiki_set.all()]
    return HttpResponse(simplejson.dumps(response), mimetype='application/json')
