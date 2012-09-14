# -*- coding: utf-8 -*-

from django.contrib import auth
from django.views.decorators.http import require_http_methods
from nbg.models import UserProxy as User
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from couchdb.http import PreconditionFailed
from urllib2 import HTTPError
from nbg.models import UserProfile, UserAction, Campus, userdb, server
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
        db = server.create('user_sync_db_{0}'.format(user.pk))

    security = db.resource.get_json('_security')[2]
    if not security:
        security = {
            'admins': {'names': [], 'roles': []},
            'readers': {'names': [], 'roles': []}, 
        }
    if not username in security['readers']['names']:
        security['readers']['names'].append(username)
        db.resource.put_json('_security', body=security)

@auth_required
@json_response
def get_user(request):
    user = request.user
    user_profile = request.user.get_profile()

    response = {
        'id': user.pk,
        'nickname': user_profile.nickname,
        'course_imported': [action.semester.pk for action in
          user.useraction_set.filter(action_type=UserAction.COURSE_IMPORTED)],
    }

    if user_profile.weibo_id:
       response.update({
           'weibo': {
               'id': user_profile.weibo_id,
               'name': user_profile.weibo_name,
               'token': user_profile.weibo_token,
            },
        })
    if user_profile.renren_id:
        response.update({
            'renren': {
                'id': user_profile.renren_id,
                'name': user_profile.renren_name,
                'token': user_profile.renren_token,
             },
         })

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
            },
        })

    return response

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
                'course_imported': [action.semester.pk for action in
                  user.useraction_set.filter(action_type=UserAction.COURSE_IMPORTED)],
            }

            if user_profile.weibo_id:
               response.update({
                   'weibo': {
                       'id': user_profile.weibo_id,
                       'name': user_profile.weibo_name,
                       'token': user_profile.weibo_token,
                    },
                })
            if user_profile.renren_id:
                response.update({
                    'renren': {
                        'id': user_profile.renren_id,
                        'name': user_profile.renren_name,
                        'token': user_profile.renren_token,
                     },
                 })

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
                    },
                })
        else:
            response = {
                'error': "帐户已被注销。",
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
        return {'error_code': 'SyntaxError'}, 400

    try:
        user = auth.authenticate(weibo_token=weibo_token)
    except HTTPError:
        return {
            'error_code': "ErrorConnectingServer",
            'error': "连接新浪微博服务器时发生错误。",
        }, 503
    except VerifyError:
        return {
            'error_code': "InvalidToken",
            'error': "新浪微博 token 错误。"
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
                'course_imported': [action.semester.pk for action in
                  user.useraction_set.filter(action_type=UserAction.COURSE_IMPORTED)],
            }

            if user_profile.weibo_token != weibo_token:
                user_profile.weibo_token = weibo_token

            if user_profile.weibo_name != weibo_name:
                user_profile.weibo_name = weibo_name

            user_profile.save()

            response.update({
               'weibo': {
                   'id': weibo_id,
                   'name': weibo_name,
                   'token': weibo_token,
                },
            })
            if user_profile.renren_id:
                response.update({
                    'renren': {
                        'id': user_profile.renren_id,
                        'name': user_profile.renren_name,
                        'token': user_profile.renren_token,
                     },
                 })

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
        return {'error_code': 'SyntaxError'}, 400

    try:
        user = auth.authenticate(renren_token=renren_token)
    except HTTPError:
        return {
            'error_code': "ErrorConnectingServer",
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
            renren_id, renren_name = get_renren_profile(renren_token)
            sync_credentials_to_couchdb(user, '-renren-{0}'.format(renren_id), renren_token)
            user_profile = user.get_profile()

            response = {
                'id': user.pk,
                'email': user.email,
                'nickname': user_profile.nickname,
                'course_imported': [action.semester.pk for action in
                  user.useraction_set.filter(action_type=UserAction.COURSE_IMPORTED)],
            }

            if user_profile.renren_token != renren_token:
                user_profile.renren_token = renren_token

            if user_profile.renren_name != renren_name:
                user_profile.renren_name = renren_name

            user_profile.save()

            if user_profile.weibo_id:
               response.update({
                   'weibo': {
                       'id': user_profile.weibo_id,
                       'name': user_profile.weibo_name,
                       'token': user_profile.weibo_token,
                    },
                })
            response.update({
                'renren': {
                    'id': renren_id,
                    'name': renren_name,
                    'token': renren_token,
                 },
             })

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
def reg(request, method):
    nickname = request.POST.get('nickname', None)
    campus_id = request.POST.get('campus_id', None)

    if not nickname:
        return {'error_code': 'SyntaxError'}, 400

    '''get necessary args, check em and create the user'''
    if method == 'email':
        email = request.POST.get('email', None)
        password = request.POST.get('password', None)
        if email and password:
            try:
                validate_email(email)
            except ValidationError:
                return {'error': 'Email 格式不正确。'}, 400

            username = email
            try:
                user = User.objects.create_user(username=username, email=email, password=password)
            except (IntegrityError, PreconditionFailed):
                return {'error': 'Email 已被使用。'}, 403

            profile_args = {}
            auth_args = {
                'username': email,
                'password': password,
            }
        else:
            return {'error_code': 'SyntaxError'}, 400
    elif method == 'weibo':
        weibo_token = request.POST.get('token', None)
        if weibo_token:
            try:
                weibo_id, weibo_name = get_weibo_profile(weibo_token)
            except HTTPError:
                return {
                    'error_code': "ErrorConnectingServer",
                    'error': "连接新浪微博服务器时发生错误。",
                }, 503
            except VerifyError:
                return {
                    'error_code': "InvalidToken",
                    'error': "新浪微博 token 错误。"
                }, 403
            if UserProfile.objects.filter(weibo_id=weibo_id).exists():
                return {
                    'error_code': "TokenAlreadyUsed",
                    'error': "新浪微博帐号已被使用。",
                }, 403

            # this password is not used for auth
            username = '-weibo-{0}'.format(weibo_id)
            password = weibo_token
            user = User.objects.create_user(username=username, password=password)

            profile_args = {
                'weibo_id': weibo_id,
                'weibo_name': weibo_name,
                'weibo_token': weibo_token,
            }
            auth_args = {
                'weibo_token': weibo_token,
            }
        else:
            return {'error_code': 'SyntaxError'}, 400
    elif method == 'renren':
        renren_token = request.POST.get('token', None)
        if renren_token:
            try:
                renren_id, renren_name = get_renren_profile(renren_token)
            except HTTPError:
                return {
                    'error_code': "ErrorConnectingServer",
                    'error': "连接人人服务器时发生错误。",
                }, 503
            except VerifyError:
                return {
                    'error_code': "InvalidToken",
                    'error': "人人 token 错误。"
                }, 403
            if UserProfile.objects.filter(renren_id=renren_id).exists():
                return {
                    'error_code': "TokenAlreadyUsed",
                    'error': "人人帐号已被使用。",
                }, 403

            # this password is not used for auth
            username = '-renren-{0}'.format(renren_id)
            password = renren_token
            user = User.objects.create_user(username=username, password=password)

            profile_args = {
                'renren_id': renren_id,
                'renren_name': renren_name,
                'renren_token': renren_token,
            }
            auth_args = {
                'renren_token': renren_token,
            }
        else:
            return {'error_code': 'SyntaxError'}, 400
    else:
        return {'error_code': 'SyntaxError'}, 400

    '''maybe wanna set campus'''
    if campus_id:
        try:
            campus = Campus.objects.get(pk=campus_id)
        except ValueError:
            return {'error_code': 'SyntaxError'}, 400
        except Campus.DoesNotExist:
            return {'error_code': 'CampusNotFound'}, 404

    '''create user profile and login the user'''
    user_profile = UserProfile(user=user, nickname=nickname, **profile_args)
    if campus_id:
        user_profile.campus = campus
    user_profile.save()

    '''login the user'''
    user = auth.authenticate(**auth_args)
    auth.login(request, user)
    sync_credentials_to_couchdb(user, username, password)

    return {'id': user.pk}

@require_http_methods(['POST'])
@auth_required
@json_response
def edit(request):
    """
    temporarily not allowed to change password, not decided when request from weibo-user and renren-user

    """
    # password = request.POST.get('password', None)
    nickname = request.POST.get('nickname', None)
    weibo_token = request.POST.get('weibo_token', None)
    renren_token = request.POST.get('renren_token', None)
    campus_id = request.POST.get('campus_id', None)
    campus_none = request.POST.get('campus_none', None)

    user = request.user
    user_profile = user.get_profile()

    # if password:
        # user.set_password(password)

    if nickname:
        user_profile.nickname = nickname

    if weibo_token:
        try:
            weibo_id, weibo_name = get_weibo_profile(weibo_token)
        except HTTPError:
            return {
                'error_code': "ErrorConnectingServer",
                'error': "连接新浪微博服务器时发生错误。",
            }, 503
        except VerifyError:
            return {
                'error_code': "InvalidToken",
                'error': "新浪微博 token 错误。",
            }, 403
        if weibo_id != user_profile.weibo_id and UserProfile.objects.filter(weibo_id=weibo_id).exists():
            return {
                'error_code': "TokenAlreadyUsed",
                'error': "新浪微博帐号已被使用。",
            }, 403
        user_profile.weibo_id = weibo_id
        user_profile.weibo_name = weibo_name
        user_profile.weibo_token = weibo_token

    if weibo_token == '':
        user_profile.weibo_id = None
        user_profile.weibo_name = ''
        user_profile.weibo_token = ''

    if renren_token:
        try:
            renren_id, renren_name = get_renren_profile(renren_token)
        except VerifyError:
            return {
                'error_code': "InvalidToken",
                'error': "人人 token 错误。",
            }, 403
        if renren_id != user_profile.renren_id and UserProfile.objects.filter(renren_id=renren_id).exists():
            return {
                'error_code': "TokenAlreadyUsed",
                'error': "人人帐号已被使用。",
            }, 403
        user_profile.renren_id = renren_id
        user_profile.renren_name = renren_name
        user_profile.renren_token = renren_token

    if renren_token == '':
        user_profile.renren_id = None
        user_profile.renren_name = ''
        user_profile.renren_token = ''

    if campus_id:
        try:
            campus_id = int(campus_id)
            campus = Campus.objects.get(pk=campus_id)
        except ValueError:
            return {'error_code': 'SyntaxError'}, 400
        except Campus.DoesNotExist:
            return {'error_code': 'CampusNotFound'}, 404

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
def deactivate(request):
    request.user.is_active = False
    request.user.save()
    auth.logout(request)
    return 0
