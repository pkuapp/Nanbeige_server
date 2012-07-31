# -*- coding: utf-8 -*-

from nbg.models import *
from datetime import datetime
from nbg.helpers import json_response

@json_response
def wiki_node(request, offset):
    node_id = int(offset)
    wikinode_obj = WikiNode.objects.get(pk=node_id)
    type = wikinode_obj.type
    if type == 'L':
        response = {
            'title': wikinode_obj.title,
            'type': wikinode_obj.type,
            'list': [{
                'title': node.title,
                'node_id': node.pk,
            } for node in wikinode_obj.wikinode_set.all()]
        }
    if type == 'A':
        response = {
            'title': wikinode_obj.title,
            'type': wikinode_obj.type,
            'content': wikinode_obj.content,
        }
    return response

@json_response
def wiki_list(request, offset):
    university_id = int(offset)
    
    try:
        university_obj = University.objects.get(pk=university_id)
    except:
        return {'error': "学校不存在。"}, 404

    response = [{
        'title': item.node.title,
        'node_id': item.node.pk,
    } for item in university_obj.wiki_set.all()]
    return response
