from django.shortcuts import render_to_response

def api_html(request):
    return render_to_response('API.html')