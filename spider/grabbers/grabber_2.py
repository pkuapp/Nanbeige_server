#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import os.path
import getpass
import re
from grabber_base import BaseParser, LoginError

class TeapotParser(BaseParser):
    """Parser for Zhejiang University.
    """
    def __init__(self):
        super(TeapotParser, self).__init__()
        self.require_captcha = True
        self.available = True
        self.url_prefix = "http://jwbinfosys.zju.edu.cn/"
        self.charset = "gb2312"

    def _fetch_img(self):
        url_captcha = self.url_prefix + "CheckCode.aspx"
        r = requests.get(url_captcha)
        self.captcha_img = r.content
        self.cookies = r.cookies

    def test(self):
        self._fetch_img()
        with open(os.path.join(os.path.dirname(__file__), 'img.txt'), 'w') as img:
            img.write(self.captcha_img)

        captcha = raw_input("Captcha: ")
        username = raw_input("Username: ")
        password = getpass.getpass('Password: ')

        self.setUp(username=username, password=password, captcha=captcha)
        try:
            response = self.run()
        except LoginError as e:
            print e.error
        else:
            with open(os.path.join(os.path.dirname(__file__), 'log.html'), 'w') as log:
                log.write(response)

    def run(self):
        url_login = self.url_prefix + "default2.aspx"
        data = {
            'TextBox1': self.username,
            'TextBox2': self.password,
            'Textbox3': self.captcha,
            'RadioButtonList1': u'学生'.encode(self.charset),
            '__EVENTTARGET': "Button1",
            '__EVENTARGUMENT': "",
            '__VIEWSTATE': "dDwtMTAzMjcxNTk2NDs7Pl+gyMxRYhv1lADUeH98zifgfUbl",
            'Text1': "",
        }
        r = requests.post(url_login, data=data, cookies=self.cookies)

        p = re.compile("<script language='javascript'>alert\('(.{,300})'\);</script>")
        result = p.match(r.content)
        if result:
            msg = result.group(1).decode(self.charset)
            if msg == u"验证码不正确！！":
                raise LoginError("captcha")
            if msg == u"用户名不存在！！":
                raise LoginError("auth")
            if msg[:4] == u"密码错误":
                raise LoginError("auth")

        return r.content

if __name__ == "__main__":
    grabber = TeapotParser()
    grabber.test()
