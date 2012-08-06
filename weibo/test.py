#!/usr/bin/env python

from weibo import APIClient

# https://api.weibo.com/oauth2/authorize?display=mobile&client_id=1362082242&&response_type=token&redirect_uri=https://api.weibo.com/oauth2/default.html

APP_KEY = '1362082242'
APP_SECRET = '26a3e4f3e784bd183aeac3d58440f19f'
CALLBACK_URL = 'http://www.example.com/callback'

# client = APIClient(app_key=APP_KEY, app_secret=APP_SECRET, redirect_uri=CALLBACK_URL)
# url = client.get_authorize_url()

# code = your.web.framework.request.get('code')
# client = APIClient(app_key=APP_KEY, app_secret=APP_SECRET, redirect_uri=CALLBACK_URL)
# r = client.request_access_token(code)
# access_token = r.access_token
# expires_in = r.expires_in

client = APIClient(app_key=APP_KEY, app_secret=APP_SECRET, redirect_uri=CALLBACK_URL)
# client.set_access_token(access_token, expires_in)
client.set_access_token("2.00vJKFEC7oJLUB8efcff4bb9ujwXBE", 4294967295)

print client.get.statuses__user_timeline()
# print client.post.statuses__update(status='Test OAuth 2.0')
# print client.upload.statuses__upload(status='Test OAuth 2.0 w/ picture.', pic=open('/Users/michael/test.png'))