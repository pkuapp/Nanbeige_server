# -*- coding: utf-8 -*-

import requests
import hashlib

API_SERVER = "http://api.renren.com/restserver.do"

class RenrenAPIClient(object):
    def __init__(self, app_key=None, app_secret=None, token=None):
        self.token = token
        self.app_key = app_key
        self.app_secret = app_secret
        self.base_params = {
            'v': '1.0',
            'format': 'JSON',
            'access_token': token,
        }

    def _post(self, url, params):
        return requests.post(url, data=params).json

    def _get(self, url):
        return requests.get(url).json

    def request(self, params):
        result = self._post(API_SERVER, self._get_params(params))
        if isinstance(result, list):
            return result[0]
        return result

    def _get_params(self, params):
        params.update(self.base_params)
        params['sig'] = self._get_sig(params)
        return params

    def _get_sig(self, params):
        return hashlib.md5(''.join(['{0}={1}'.format(x, params[x])
          for x in sorted(params.keys())]) + self.app_secret).hexdigest()

class RenrenAPIError(Exception):
    def __init__(self, code, message):
        Exception.__init__(self, message)
        self.code = code
