# -*- coding: utf-8 -*-

from django.contrib import auth
from django.views.decorators.http import require_http_methods
from nbg.models import UserProxy as User
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from couchdb.http import PreconditionFailed
from urllib2 import HTTPError
from nbg.models import UserProfile, Campus, userdb, server
from nbg.helpers import json_response, auth_required
from sns.verifiers import VerifyError, get_weibo_profile, get_renren_profile

def sync_credentials_to_couchdb(user, username, password_or_token):
    from couchdb.http import ResourceNotFound
    user_id = 'org.couchdb.user:{0}'.format(username)
    doc = {
        '_id': user_id,
        'type': 'user',
        'roles': [],
        'name': username,
        'password': password_or_token,
    }
    try:
        doc = userdb[user_id]
        doc['_rev'] = doc.rev
        userdb.save(doc)
    except ResourceNotFound:
        userdb.save(doc)
    try:
        db = server['user_sync_db_{0}'.format(user.pk)]
    except ResourceNotFound:
        server.create('user_sync_db_{0}'.format(user.pk))

    security = db.resource.get_json('_security')[2]
    if not security:
        security = {
            'admins': {'names': [], 'roles': []},
            'readers': {'names': [], 'roles': []}, 
        }
    if not username in security['readers']['names']:
        security['readers']['names'].append(username)
        db.resource.put_json('_security',body=security)

@auth_required
@json_response
def get_user(request):
    return {'id': request.user.pk}

@require_http_methods(['POST'])
@json_response
def login_email(request):
    username = request.POST.get('email', '')
    password = request.POST.get('password', '')

    if username.find(':') >= 0:
        return {
            'error': "Email 或密码错误。",
        }, 403

    user = auth.authenticate(username=username, password=password)

    if user is not None:
        if user.is_active:
            auth.login(request, user)
            sync_credentials_to_couchdb(user, user.email, password)
            user_profile = user.get_profile()

            response = {
                'id': user.pk,
                'email': user.email,
                'nickname': user_profile.nickname,
            }

            user_profile.weibo_id and response.update({'weibo_id': user_profile.weibo_id}) 
            user_profile.weibo_name and response.update({'weibo_name': user_profile.weibo_name})

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
    weibo_token = request.POST.get('token', None)
    if not weibo_token:
        return {'error': '缺少必要的参数。'}, 400

    try:
        user = auth.authenticate(weibo_token=weibo_token)
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
            weibo_id, weibo_name = get_weibo_profile(weibo_token)
            sync_credentials_to_couchdb(user, '-weibo-{0}'.format(weibo_id), weibo_token)
            user_profile = user.get_profile()

            response = {
                'id': user.pk,
                'email': user.email,
                'nickname': user_profile.nickname,
                'weibo_id': weibo_id,
                'weibo_name': weibo_name,
            }

            if not user_profile.weibo_id or not user_profile.weibo_name:
                user_profile.weibo_id = weibo_id
                user_profile.weibo_name = weibo_name
                user_profile.save()
            
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
def login_renren(request):
    renren_token = request.POST.get('token', None)
    if not renren_token:
        return {'error': '缺少必要的参数。'}, 400

    try:
        user = auth.authenticate(renren_token=renren_token)
    except HTTPError:
        return {
            'error_code': "ErrorConnectingWeiboServer",
            'error': "连接人人服务器时发生错误。",
        }, 503
    except VerifyError:
        return {
            'error_code': "InvalidToken",
            'error': "人人 token 错误。"
        }, 403

    if user is not None:
        if user.is_active:
            auth.login(request, user)
            renren_id, name = get_renren_profile(renren_token)
            sync_credentials_to_couchdb(user, '-renren-{0}'.format(renren_id), renren_token)
            user_profile = user.get_profile()

            response = {
                'id': user.pk,
                'email': user.email,
                'nickname': user_profile.nickname,
                'renren_id': renren_id,
                'renren_name': name,
            }

            if not user_profile.renren_id or not user_profile.renren_name:
                user_profile.renren_id = renren_id
                user_profile.renren_name = name
                user_profile.save()
            
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
        if len(email) > 70:
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
        except (IntegrityError, PreconditionFailed):
            return {'error': 'Email 已被使用。'}, 403
        user_profile = UserProfile.objects.create(user=user, nickname=nickname)
        if campus_id:
            user_profile.campus = campus
            user_profile.save()

        user = auth.authenticate(username=email, password=password)
        auth.login(request, user)
        sync_credentials_to_couchdb(user, email, password)

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
            user = User.objects.create_user(username='-weibo-{0}'.format(weibo_id), password=token)
        except IntegrityError:
            return {'error': '微博帐号已被使用。'}, 403
        UserProfile.objects.create(user=user, weibo_id=weibo_id,\
            nickname=nickname, weibo_name=screen_name)

        user = auth.authenticate(weibo_token=token)
        auth.login(request, user)
        sync_credentials_to_couchdb(user, '-weibo-{0}'.format(weibo_id), token)
        return {'id': user.pk}
    else:
        return {'error_code': "BadSyntax"}, 400

@require_http_methods(['POST'])
@json_response
def reg_renren(request):
    token = request.POST.get('token', None)
    nickname = request.POST.get('nickname', None)

    if token and nickname:
        try:
            renren_id, name = get_renren_profile(token)
        except HTTPError:
            return {
                'error_code': "ErrorConnectingWeiboServer",
                'error': "连接人人服务器时发生错误。",
            }, 503
        except VerifyError:
            return {
                'error_code': "InvalidToken",
                'error': "人人 token 错误。"
            }, 403

        try:
            # this password is not used for auth
            user = User.objects.create_user(username='-renren-{0}'.format(renren_id), password=token)
        except IntegrityError:
            return {'error': '人人帐号已被使用。'}, 403
        UserProfile.objects.create(user=user, renren_id=renren_id,\
            nickname=nickname, renren_name=name)

        user = auth.authenticate(renren_token=token)
        auth.login(request, user)
        sync_credentials_to_couchdb(user, '-renren-{0}'.format(renren_id), token)
        return {'id': user.pk}
    else:
        return {'error_code': "BadSyntax"}, 400

@require_http_methods(['POST'])
@auth_required
@json_response
def edit(request):
    """
    temporarily not allowed to change password, not decided when request from weibo-user and renren-user

    """
    # password = request.POST.get('password', None)
    nickname = request.POST.get('nickname', None)
    # weibo_token = request.POST.get('weibo_token', None)
    campus_id = request.POST.get('campus_id', None)
    campus_none = request.POST.get('campus_none', None)

    user = request.user
    user_profile = user.get_profile()

    # if password:
        # user.set_password(password)

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
