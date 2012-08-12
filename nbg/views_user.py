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
from sns.verifiers import VerifyError, get_weibo_profile

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
            user_profile = user.get_profile()

            response = {
                'id': user.pk,
                'email': user.email,
                'nickname': user_profile.nickname,
            }

            user_profile.id && response['weibo_id'] = weibo_id
            user_profile.name && response['weibo_name'] = weibo_name
            
            campus = user_profile.campus
            if campus:
                response.update({
                    'university': {
                            'id': campus.university.pk,
                            'name': campus.university.name,
                    },
                    'campus': {
                            'id': campus.pk,
                            'name': campus.name
                    }
                })
        else:
            response = {
                'error': "用户已被吊销。",
            }, 403
    else:
        response = {
            'error': "Email 或密码错误。",
        }, 403

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
        }, 503
    except VerifyError:
        return {
            'error_code': "InvalidToken",
            'error': "微博 token 错误。"
        }, 403

    if user is not None:
        if user.is_active:
            auth.login(request, user)
            user_profile = user.get_profile()

            response = {
                'id': user.pk,
                'email': user.email,
                'nickname': user_profile.nickname,
            }

            user_profile.id && response['weibo_id'] = weibo_id
            user_profile.name && response['weibo_name'] = weibo_name

            campus = user_profile.campus
            if campus:
                response.update({
                    'university': {
                            'id': campus.university.pk,
                            'name': campus.university.name,
                    },
                    'campus': {
                            'id': campus.pk,
                            'name': campus.name
                    }
                })
        else:
            response = {
                'error': "用户已被吊销。",
            }, 403
    else:
        response = {
            'error_code': "UserNotFound",
        }, 403

    return response

@require_http_methods(['POST'])
@json_response
def reg_email(request):
    email = request.POST.get('email', None)
    nickname = request.POST.get('nickname', None)
    password = request.POST.get('password', None)
    campus_id = request.POST.get('campus_id', None)

    if email and nickname and password:
        try:
            validate_email(email)
        except ValidationError:
            return {'error': 'Email 格式不正确。'}, 400
        if len(email) > 30:
            return {'error': 'Email 地址过长。'}, 400

        if campus_id:
            try:
                campus = Campus.objects.get(pk=campus_id)
            except ValueError:
                return {'error_code': 'BadSyntax'}, 400
            except Campus.DoesNotExist:
                return {'error_code': 'CampusNotFound'}, 400

        try:
            user = User.objects.create_user(username=email, email=email, password=password)
        except IntegrityError:
            return {'error': 'Email 已被使用。'}, 403
        user_profile = UserProfile.objects.create(user=user, nickname=nickname)
        if campus_id:
            user_profile.campus = campus
            user_profile.save()

        user = auth.authenticate(username=email, password=password)
        auth.login(request, user)

        return {'id': user.pk}
    else:
        return {'error_code': "BadSyntax"}, 400

@require_http_methods(['POST'])
@json_response
def reg_weibo(request):
    token = request.POST.get('token', None)
    nickname = request.POST.get('nickname', None)

    if token and nickname:
        try:
            weibo_id, screen_name = get_weibo_profile(token)
        except HTTPError:
            return {
                'error_code': "ErrorConnectingWeiboServer",
                'error': "连接微博服务器时发生错误。",
            }, 503
        except VerifyError:
            return {
                'error_code': "InvalidToken",
                'error': "微博 token 错误。"
            }, 403

        try:
            # this password is not used for auth
            user = User.objects.create_user(username=weibo_id, password="WeiboUser")
        except IntegrityError:
            return {'error': '微博帐号已被使用。'}, 403
        UserProfile.objects.create(user=user, weibo_id=weibo_id,\
            nickname=nickname, weibo_name=screen_name)

        user = auth.authenticate(weibo_token=token)
        auth.login(request, user)

        return {'id': user.pk}
    else:
        return {'error_code': "BadSyntax"}, 400

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
