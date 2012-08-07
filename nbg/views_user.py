# -*- coding: utf-8 -*-

from django.contrib import auth
from django.views.decorators.http import require_http_methods
from django.contrib.auth.models import User
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from urllib2 import HTTPError
from nbg.models import UserProfile, Campus
from nbg.helpers import json_response, auth_required
from sns.verifiers import VerifyError, get_weibo_uid

@auth_required
@json_response
def get_user(request):
    return {'id': request.user.pk}

@require_http_methods(['POST'])
@json_response
def login_email(request):
    username = request.POST.get('email', '')
    password = request.POST.get('password', '')

    user = auth.authenticate(username=username, password=password)

    if user is not None:
        if user.is_active:
            auth.login(request, user)
            response = {
                'id': user.pk,
                'nickname': user.get_profile().nickname,
                'university': None,
            }
            campus = user.get_profile().campus
            if campus:
                response['university'] = {
                    'id': campus.university.pk,
                    'name': campus.university.name,
                }
        else:
            response = {
                'error': "用户已被吊销。",
            }, 401
    else:
        response = {
            'error': "Email 或密码错误。",
        }, 401

    return response

@require_http_methods(['POST'])
@json_response
def login_weibo(request):
    token = request.POST.get('token', None)
    if not token:
        return {'error': '缺少必要的参数。'}, 400

    try:
        user = auth.authenticate(weibo_token=token)
    except HTTPError:
        return {
            'error_code': "ErrorConnectingWeiboServer",
            'error': "连接微博服务器时发生错误。",
        }, 500
    except VerifyError:
        return {
            'error_string': "InvalidToken",
            'error': "微博 token 错误。"
        }, 403

    if user:
        auth.login(request, user)
    else:
        return {
            'error_code': "UserNotFound",
        }, 401

    return 0

@require_http_methods(['POST'])
@json_response
def reg_email(request):
    email = request.POST.get('email', None)
    nickname = request.POST.get('nickname', None)
    password = request.POST.get('password', None)

    if email and nickname and password:
        try:
            validate_email(email)
        except ValidationError:
            return {'error': 'Email 格式不正确。'}, 400
        if len(email) > 30:
            return {'error': 'Email 地址过长。'}, 400

        try:
            user = User.objects.create_user(username=email, email=email, password=password)
        except IntegrityError:
            return {'error': 'Email 已被使用。'}, 403
        UserProfile.objects.create(user=user, nickname=nickname)

        user = auth.authenticate(username=email, password=password)
        auth.login(request, user)

        return {'id': user.pk}
    else:
        return {'error': '缺少必要的参数。'}, 400

@require_http_methods(['POST'])
@auth_required
@json_response
def edit(request):
    password = request.POST.get('password', None)
    nickname = request.POST.get('nickname', None)
    # weibo_token = request.POST.get('weibo_token', None)
    campus_id = request.POST.get('campus_id', None)
    campus_none = request.POST.get('campus_none', None)

    user = request.user
    user_profile = user.get_profile()

    if password:
        user.set_password(password)

    if nickname:
        user_profile.nickname = nickname

    # if weibo_token:
    #     user_profile.weibo_token = weibo_token

    if campus_id:
        try:
            campus_id = int(campus_id)
            campus = Campus.objects.get(pk=campus_id)
        except ValueError:
            return {'error': 'campus_id 参数格式不正确。'}, 400
        except Campus.DoesNotExist:
            return {'error': '校区不存在。'}, 404

        user_profile.campus = campus

    if campus_none == '1':
        user_profile.campus = None

    user.save()
    user_profile.save()

    return 0

@require_http_methods(['POST'])
@auth_required
@json_response
def logout(request):
    auth.logout(request)
    return 0

@require_http_methods(['POST'])
@auth_required
@json_response
def deactive(request):
    request.user.is_active = False
    request.user.save()
    auth.logout(request)
    return 0
