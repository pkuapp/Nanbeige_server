#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
from grabber_base import BaseParser

class TeapotParser(BaseParser):
    """Parser for Zhejiang University.
    """
    def __init__(self):
        super(TeapotParser, self).__init__()
        self.require_captcha = True
        self.available = True
        self.url_prefix = "http://jwbinfosys.zju.edu.cn/"

    def _fetch_img(self):
        headers = {'User-Agent': self.ua}
        url_captcha = self.url_prefix + "CheckCode.aspx"
        resp = requests.get(url_captcha, headers=headers)
        self.captcha_img = resp.content

    def run(self):
        self._fetch_img()

if __name__ == "__main__":
    grabber = TeapotParser()
    grabber.run()
