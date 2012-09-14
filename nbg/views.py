from django.shortcuts import render_to_response

def doc_html(request):
    response = render_to_response('doc.html')
    response.status_code = 418
    return response
