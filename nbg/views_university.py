# -*- coding:UTF-8 -*-

from django.http import HttpResponse
from django.utils import simplejson
from nbg.models import *
from datetime import datetime

def university_list(request):
    try:
        university_values = University.objects.values()
        response = [{'id': item['id'], 'name': item['name'], 'location': {'latitude': float(item['latitude']), 'longitude': float(item['longitude'])}} for item in university_values]
        return HttpResponse(simplejson.dumps(response, sort_keys=True), mimetype = 'application/json')
    except:
        return HttpResponse(simplejson.dumps({'error': '尚无数据'}), mimetype='application/json')

def detail(request, offset):
    university_id = int(offset)
    if university_id:
        try:
            university_detail = University.objects.filter(id=university_id).values()
            response = [{
                'name': item['name'],
                'location': {
                    'latitude': float(item['latitude']),
                    'longitude': float(item['longitude'])},
                'support': {
                    'import_course': item['support_import_course'],
                    'list_course': item['support_list_course']},
                'week': {
                    'start': datetime.strftime(item['week_start'] , '%Y-%m-%d'),
                }
            } for item in university_detail]
            return HttpResponse(simplejson.dumps(response), mimetype = 'application/json')
        except:
            raise
        else:
            pass
        finally:
            pass
    else:
        return HttpResponse("haha")


#def detail(request):
 #   return HttpResponse(simplejson.dumps({'name':'Peking University','location':{'latitude':'116.3018 E','longitude':'39.9712 N'},
  #          'support':{'import_course':'fill in a boolean variant','list_course':'fill in a boolean variant'},'week':{'start':'yyyy-mm-dd','end':'yyyy-mm-dd','excluded':'[xxxx]'},'lessons':{'count':{'total':'13','morning':'5','afternoon':'5','night':'3'}},'detail':[{'number':'1','start':'0800','end':'0845'},'...',{'number':'13','start':'2010','end':'2055'}]}),mimetype='application/json',)
