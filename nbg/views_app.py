from django.http import HttpResponse
from django.utils import simplejson

def version_api(request):
	return HttpResponse(simplejson.dumps({'version':'9'}),mimetype='application/json')