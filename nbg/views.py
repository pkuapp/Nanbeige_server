from django.shortcuts import render_to_response

def doc_html(request):
    return render_to_response('doc.html')

def status_html(request):
    return render_to_response('status.html')
