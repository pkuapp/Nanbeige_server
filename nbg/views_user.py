# -*- coding: utf-8 -*-

from django.http import HttpResponse
from django.contrib import auth
from django.views.decorators.http import require_http_methods

@require_http_methods(['POST'])
def login_email(request):
    username = request.POST.get('email', '')
    password = request.POST.get('password', '')

    user = auth.authenticate(username=username, password=password)
    if user is not None and user.is_active:
        auth.login(request, user)
        return HttpResponse("1")
    else:
        return HttpResponse("0")