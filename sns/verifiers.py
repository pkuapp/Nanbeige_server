#!/usr/bin/env python

from urllib2 import HTTPError
from weibo import APIClient

END_OF_THE_WORLD = 4294967295

class VerifyError(Exception):
    '''
    raise VerifyError if token is invalid.
    '''
    def __init__(self, error):
        self.error = error

    def __str__(self):
        return 'VerifyError: {}'.format(self.error)

def get_weibo_uid(token):
    APP_KEY = '1362082242'
    APP_SECRET = '26a3e4f3e784bd183aeac3d58440f19f'
    CALLBACK_URL = 'http://www.example.com/callback'

    client = APIClient(app_key=APP_KEY, app_secret=APP_SECRET, redirect_uri=CALLBACK_URL)
    client.set_access_token(token, END_OF_THE_WORLD)
    try:
        ret = client.get.account__get_uid()
    except HTTPError as e:
        if e.code == 403:
            raise VerifyError("Invalid weibo token.")
        else:
            raise
    else:
        return int(ret.uid)

def get_renren_uid():
    pass

if __name__ == "__main__":
    print "Hi!"
    print get_weibo_uid("token")
