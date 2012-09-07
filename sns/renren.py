# -*- coding: utf-8 -*-

import urllib2  
import urllib  
import cookielib  
import json
import hashlib

RENREN_APP_API_KEY = "d5b688951dc4406983fdc536fe64e229"
RENREN_APP_SECRET_KEY = "6885dc0d0c1b4c35ab71e5fe1cddd8ee"

AUTHORIZATION_URI = "http://graph.renren.com/oauth/authorize"
ACCESS_TOKEN_URI = "http://graph.renren.com/oauth/token"
SESSION_KEY_URI = "http://graph.renren.com/renren_api/session_key"
API_SERVER = "http://api.renren.com/restserver.do"

class RenRenAPIClient(object):
    def __init__(self, app_key=None, app_secret=None, token=None):  
        self.cookie = cookielib.LWPCookieJar()  
        self.opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.cookie))  
        urllib2.install_opener(self.opener)
        self.token = token
        self.app_secret = app_secret

    def _post(self, url, params):  
        return self.opener.open(urllib2.Request(url, urllib.urlencode(params))).read()
  
    def _get(self, url):  
        return self.opener.open(urllib2.Request(url)).read()

    def request(self, params):
        result = json.loads(self._post(API_SERVER, self._getParams(params)))  
        if isinstance(result, list):  
            return result[0]  
        return result

    def _getParams(self, params):  
        params['sig'] = self._getSig(params)  
        return params  
  
    def _getSig(self, params):
        return hashlib.md5(''.join(['%s=%s' % (x, params[x])   
            for x in sorted(params.keys())]) + self.app_secret).hexdigest() 
    
class RenRenAPIError(Exception):
    def __init__(self, code, message):
        Exception.__init__(self, message)
        self.code = code
