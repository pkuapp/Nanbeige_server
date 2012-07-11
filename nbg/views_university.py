# -*- coding:UTF-8 -*-
from django.http import HttpResponse
from django.utils import simplejson

def university_list(request):
    return HttpResponse(simplejson.dumps({'id':'1','name':'Peking University','location':{'latitude':'116.3018 E','longitude':'39.9712 N'}}),mimetype='application/json')

def detail(request):
    return HttpResponse(simplejson.dumps({'name':'Peking University','location':{'latitude':'116.3018 E','longitude':'39.9712 N'},
            'support':{'import_course':'fill in a boolean variant','list_course':'fill in a boolean variant'},'week':{'start':'yyyy-mm-dd','end':'yyyy-mm-dd','excluded':'[xxxx]'},'lessons':{'count':{'total':'13','morning':'5','afternoon':'5','night':'3'}},'detail':[{'number':'1','start':'0800','end':'0845'},'...',{'number':'13','start':'2010','end':'2055'}]}),mimetype='application/json',)
