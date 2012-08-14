from urllib2 import HTTPError
from verifiers import get_weibo_profile, VerifyError
from nbg.models import UserProxy as User
from nbg.models import UserProfile

class EmailBackend(object):
    supports_object_permissions = False
    supports_anonymous_user = False
    supports_inactive_user = False

    def authenticate(self, username=None, password=None):
        try:
            user = User.objects.get(email=username)
        except User.DoesNotExist:
            return None
        return user

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None

class WeiboBackend(object):
    supports_object_permissions = False
    supports_anonymous_user = False
    supports_inactive_user = False

    def authenticate(self, weibo_token=None):
        if weibo_token:
            weibo_id, screen_name = get_weibo_profile(weibo_token)
            
            try:
                user_profile = UserProfile.objects.get(weibo_id=weibo_id)
            except UserProfile.DoesNotExist:
                # password could be anything, cuz it won't be checked
                # user = User(username=weibo_id, weibo_id=weibo_id, password='password')
                # user.save()
                return None
            return user_profile.user
        return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
