# -*- coding: utf-8 -*-

from django.contrib import auth
from django.views.decorators.http import require_http_methods
from nbg.helpers import json_response, auth_required

@require_http_methods(['POST'])
@json_response
def login_email(request):
    username = request.POST.get('email', '')
    password = request.POST.get('password', '')

    user = auth.authenticate(username=username, password=password)
    if user is not None and user.is_active:
        auth.login(request, user)
        response = {
            'id': user.pk,
            'nickname': user.get_profile().nickname,
            'university': {
                'id': user.get_profile().university.pk,
                'name': user.get_profile().university.name,
            },
        }
    else:
        response = {
            'error': "Email 或密码错误。",
        }, 401
    return response

@require_http_methods(['POST'])
@auth_required
@json_response
def logout(request):
    auth.logout(request)
    return 0