#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os.path
from grabber_base import BaseParser

class TeapotParser(BaseParser):
    """Parser for Zhejiang University.
    """
    def __init__(self):
        super(TeapotParser, self).__init__()
        self.require_captcha = True
        self.available = True

    def _fetch_img(self):
        img = open(os.path.join(os.path.dirname(__file__), 'captcha_teapot.png'))
        self.captcha_img = img.read()

    def run(self):
        url_prefix = "http://jwbinfosys.zju.edu.cn/"
        url = url_prefix + "default2.aspx"
        return []

if __name__ == "__main__":
    grabber = TeapotParser()
    print grabber.run()
