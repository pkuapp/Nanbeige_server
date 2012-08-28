# -*- coding: utf-8 -*-

import os.path
import getpass

class LoginError(Exception):
    '''raise LoginError if error occurs in login process.
    '''
    def __init__(self, error):
        self.error = error

    def __str__(self):
        return 'LoginError: {}'.format(self.error)

class GrabError(Exception):
    '''raise GrabError if error occurs in grab process.
    '''
    def __init__(self, error):
        self.error = error

    def __str__(self):
        return 'GrabError: {}'.format(self.error)

class BaseParser(object):
    """All your grabber are belong to us.

    Grabbers may be used outside of django environment as standalone script.
    Do not import packages depend on django.

    Usage:
    1. Frontend calls work_flow_type() then self.captcha_img will be set AUTOMATICALLY
    if require_captcha is set.

    2. Frontend calls setUp() and provides username, password and captcha if required.
    3. Frontend calls run() and then get attr courses for list or get an exception if anything goes wrong.

    For override:
    1. In your __init__() method, set require_captcha to True if a captcha is required.
    More require_xxx option may be added in the future.
    Or, if there's anything wrong with the script for the corresponding university, set self.available to False
    and provide error info.
    2. Say the captcha is required, you MUST override *_fetch_img()* and set self.captcha_img in it.
    3. You MUST override *semester_id* to match the semester id in database.
    """
    def __init__(self):
        super(BaseParser, self).__init__()
        self.require_captcha = False
        self.available = True
        self.semester_id = 0 
        self.error = None
        self.captcha_img = None
        self.courses = None
        self.ua = r'Mozilla/5.0 (Ubuntu; Linux x86_64) TeapotParser'

    def setUp(self, **kwargs):
        self.username = kwargs['username']
        self.password = kwargs['password']
        if self.require_captcha:
            try:
                self.captcha = kwargs['captcha']
            except:
                raise LookupError('Captcha required.')

    def _local_setup(self):
        self._fetch_img()
        with open(os.path.join(os.path.dirname(__file__), 'img.gif'), 'w') as img:
            img.write(self.captcha_img)

        captcha = raw_input("Captcha: ")
        username = raw_input("Username: ")
        password = getpass.getpass('Password: ')

        self.setUp(username=username, password=password, captcha=captcha)

    def run(self):
        """Implement your request and parse code here.

        Override and SET *self.courses* with courses list with each in the following format:
        {
          "orig_id": "2011-325763QR",
          "name": "21天精通阿拉伯语（变态冲刺班）",
          "credit": 2.5,
          "teacher": "张塔,ZHANG Ta",
          "ta": "塔,Ta,宝塔",
          "lessons":
          [
            {
              "day": 5,
              "start": 1,
              "end": 2,
              "location": "牛街清真寺广场",
              "weekset_id": 9,
            },
            {
              "day": 1,
              "start": 1,
              "end": 5,
              "location": "张塔家中",
              "weekset_id": 10,
            },
          ],
        }
        """
        return []

    def _fetch_img(self):
        """Implement a valid method to fetch captcha img if require_captcha is set.

        Override and set self.img when called.
        """
        pass

    def work_flow_type(self):
        if not self.require_captcha:
            return {
                'available': self.available,
                'info': self.error,
            }

        if self.require_captcha:
            self._fetch_img()
            return {
                'available': self.available,
                'require_captcha': True,
                'info': self.error
            }

class TeapotParser(BaseParser):
    """An example parser shows how to override BaseParser.
    """
    def __init__(self):
        super(TeapotParser, self).__init__()
        self.require_captcha = True
        self.available = True

    def _fetch_img(self):
        img = open(os.path.join(os.path.dirname(__file__), 'captcha_teapot.png'))
        self.captcha_img = img.read()

    def run(self):
        return [{
            "orig_id": "2011-325763QR",
            "name": "21天精通阿拉伯语（变态冲刺班）",
            "credit": 2.5,
            "teacher":
            [
                "张塔",
                "ZHANG Ta"
            ],
            "ta":
            [
                "塔"
            ],
            "semester_id": 2,
            "lessons":
            [
                {
                    "day": 5,
                    "start": 1,
                    "end": 2,
                    "location": "牛街清真寺广场",
                    "weeks": [1, 3, 5, 7, 9, 11, 13, 15, 17]
                },
                {
                    "day": 1,
                    "start": 1,
                    "end": 5,
                    "location": "张塔家中",
                    "weeks": [1, 2, 3, 4, 5, 6, 7, 8]
                }
            ]
        },]