#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import os.path
import re
import string
from bs4 import BeautifulSoup, SoupStrainer
from helpers import pretty_print, pretty_format, chinese_weekdays, list_to_comma_separated
from grabber_base import BaseParser, LoginError, GrabError

class TeapotParser(BaseParser):
    """Parser for Beijing University of Posts and Telecommunications.
    """
    def __init__(self):
        super(TeapotParser, self).__init__()
        self.require_captcha = True
        self.available = True
        self.semester_id = 9
        self.url_prefix = ""
        self.charset = "utf8"
    def _fetch_img(self):
        with open('spider/grabbers/captcha_teapot.png') as img:
            self.captcha_img = img.read()

    def run(self):
        self._login()

        self.courses = [
                {
                    "lessons": [
                        {
                            "start": 1,
                            "end": 2,
                            "location": "主校区主楼",
                            "weekset_id": None,
                            "weeks_display": "第1-8周",
                            "weeks": "1,2,3,4,5,6,7,8",
                            "day": 1
                        },
                        {
                            "start": 5,
                            "end": 6,
                            "location": "主校区主楼",
                            "weekset_id": None,
                            "weeks_display": "第1-8周",
                            "weeks": "1,2,3,4,5,6,7,8",
                            "day": 3
                        }
                    ],
                    "credit": 2,
                    "name": "沏茶理论 I",
                    "original_id": "TEA1",
                    "ta": "茶杯！",
                    "id": 22530,
                    "teacher": "茶壶",
                },
                {
                    "lessons": [
                        {
                            "start": 10,
                            "end": 11,
                            "location": "主校区主楼",
                            "weekset_id": None,
                            "weeks_display": "第1-8周",
                            "weeks": "1,2,3,4,5,6,7,8",
                            "day": 2
                        },
                        {
                            "start": 10,
                            "end": 11,
                            "location": "主校区主楼",
                            "weekset_id": None,
                            "weeks_display": "第1-8周",
                            "weeks": "1,2,3,4,5,6,7,8",
                            "day": 4
                        }
                    ],
                    "credit": 3.5,
                    "name": "煮咖啡技巧 I",
                    "original_id": "COF1",
                    "ta": "咖啡杯",
                    "id": 22531,
                    "teacher": "咖啡壶",
                },
                {
                    "lessons": [
                        {
                            "start": 3,
                            "end": 4,
                            "location": "主校区主楼",
                            "weekset_id": None,
                            "weeks_display": "第1-8周",
                            "weeks": "1,2,3,4,5,6,7,8",
                            "day": 2
                        },
                        {
                            "start": 5,
                            "end": 6,
                            "location": "主校区主楼",
                            "weekset_id": None,
                            "weeks_display": "第1-8周",
                            "weeks": "1,2,3,4,5,6,7,8",
                            "day": 1
                        },
                        {
                            "start": 7,
                            "end": 9,
                            "location": "主校区主楼",
                            "weekset_id": None,
                            "weeks_display": "第1-8周",
                            "weeks": "1,2,3,4,5,6,7,8",
                            "day": 5
                        }
                    ],
                    "credit": 4,
                    "name": "超文本咖啡壶协议基础 I",
                    "original_id": "HTCPCP1",
                    "ta": "咖啡杯",
                    "id": 22532,
                    "teacher": "电控咖啡壶"
                }]
        return self.courses

    def _login(self):
        data = {
            'username': self.username,
            'password': self.password,
            'captcha': self.captcha,
        }
        if self.username == 'teapot' and self.password == 'coffee' and self.captcha == 'teapot':
            print "Logged in successfully."
        else:
            raise LoginError('Unable to login.')
