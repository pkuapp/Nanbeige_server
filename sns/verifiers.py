#!/usr/bin/env python

from urllib2 import HTTPError
from weibo import APIClient
from renren import RenRenAPIClient

END_OF_THE_WORLD = 4294967295

class VerifyError(Exception):
    '''raise VerifyError if token is invalid.
    '''
    def __init__(self, error):
        self.error = error

    def __str__(self):
        return 'VerifyError: {}'.format(self.error)

def get_weibo_profile(token):
    APP_KEY = '1362082242'
    APP_SECRET = '26a3e4f3e784bd183aeac3d58440f19f'
    CALLBACK_URL = 'http://www.example.com/callback'

    client = APIClient(app_key=APP_KEY, app_secret=APP_SECRET, redirect_uri=CALLBACK_URL)
    client.set_access_token(token, END_OF_THE_WORLD)
    try:
        ret = client.get.account__get_uid()
        profile = client.get.users__show(uid=ret.uid)#.screen_name
        # ret = client.get.statuses__friends_timeline()
    except HTTPError as e:
        if e.code == 403:
            raise VerifyError("Invalid weibo token.")
        else:
            raise
    else:
        return ret.uid, profile.screen_name

def get_renren_profile(token):
    APP_KEY = 'd5b688951dc4406983fdc536fe64e229'
    APP_SECRET = '6885dc0d0c1b4c35ab71e5fe1cddd8ee'
    client = RenRenAPIClient(app_key=APP_KEY, app_secret=APP_SECRET, token=token)
    try:
        ret = client.request({'access_token':token,  
            'method':'users.getInfo', 'v':'1.0', 'format':'JSON'})
    except HTTPError as e:
        raise VerifyError('failed connecting to RenRen')
    else:
        return ret['uid'], ret['name']

if __name__ == "__main__":
    print "Hi!"
    print get_renren_profile("201965|6.de37dab2e72a240328a65b986b4b5fdf.2592000.1347714000-270474396")
