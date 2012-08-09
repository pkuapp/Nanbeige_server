#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import os.path
import re
from bs4 import BeautifulSoup, SoupStrainer
from helpers import pretty_print, chinese_week_numbers
from grabber_base import BaseParser, LoginError

class TeapotParser(BaseParser):
    """Parser for Zhejiang University.
    """
    def __init__(self):
        super(TeapotParser, self).__init__()
        self.require_captcha = True
        self.available = True
        self.url_prefix = "http://jwbinfosys.zju.edu.cn/"
        self.charset = "gbk"

    def _fetch_img(self):
        url_captcha = self.url_prefix + "CheckCode.aspx"
        r = requests.get(url_captcha)
        self.captcha_img = r.content
        self.cookies = r.cookies

    def test(self):
        self._local_setup()

        try:
            response = self.run()
        except LoginError as e:
            print e.error
        else:
            with open(os.path.join(os.path.dirname(__file__), 'log.html'), 'w') as log:
                log.write(response)

    @staticmethod
    def trim_location(l):
        l = l.replace(u"(网络五边菱)", "")
        l = l.replace(u"(五边菱形)", "")
        l = l.replace(u"(六边圆形)", "")
        l = l.replace(u"(普)", "")
        l = l.replace(u"(多)", "")
        l = l.replace("*", "")
        return l

    def grab_all(self):
        self._local_setup()
        self._login()

        url_courses = self.url_prefix + "jxrw_zd.aspx?xh=" + self.username

        '''get viewstate'''
        r_viewstate = requests.get(url_courses, cookies=self.cookies)
        result = re.search('<input type="hidden" name="__VIEWSTATE" value="(.+)" />', r_viewstate.content)
        viewstate = result.group(1)

        print "Get viewstate: done."

        data = {
            '__EVENTTARGET': "",
            '__EVENTARGUMENT': "",
            '__VIEWSTATE': viewstate,
            'ddlXN': "2012-2013",
            'ddlXQ': "1",
            'ddlXY': u'本科生院'.encode(self.charset),
            'ddlZY': "",
            'ddlKC': "",
            'btnFilter': u' 查 询 '.encode(self.charset),
        }
        r_courses = requests.post(url_courses, data=data, cookies=self.cookies)

        with open(os.path.join(os.path.dirname(__file__), 'log.html'), 'w') as log:
            log.write(r_courses.content)

    def _login(self):
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
        r_login = requests.post(url_login, data=data, cookies=self.cookies)

        result = re.match("<script language='javascript'>alert\('(.{,300})'\);</script>", r_login.content)
        if result:
            msg = result.group(1).decode(self.charset)
            if msg == u"验证码不正确！！":
                raise LoginError("captcha")
            if msg == u"用户名不存在！！":
                raise LoginError("auth")
            if msg[:4] == u"密码错误":
                raise LoginError("auth")
        content = r_login.content.decode(self.charset)
        if u"欢迎您来到现代教务管理系统！" not in content:
            raise LoginError("unknown")
        '''logged in successfully'''
        print "Logged in successfully."
        self.cookies = r_login.cookies

    def run(self):
        self._login()

        url_course = self.url_prefix + "xskbcx.aspx?xh=" + self.username
        r_course = requests.get(url_course, cookies=self.cookies)

        '''parse'''
        strainer = SoupStrainer("table", id="xsgrid")
        soup = BeautifulSoup(r_course.content, parse_only=strainer)
        rows = soup.select("tr")
        courses = []
        for r in rows:
            if r.has_key('class') and r['class'] == ["datagridhead"]:
                continue

            cols = r.select("td")
            semester_text = cols[3].get_text(strip=True)
            time_texts = [text for text in cols[4].stripped_strings]
            locations = [text for text in cols[5].stripped_strings]

            '''parse lesson'''
            ''' - parse time'''
            lessons = []
            for time_text in time_texts:
                '''parse week'''
                '''data for 2012-2013, should be updated every year
                first week: 2012-09-10
                '''
                week_data = {
                    u"秋": {
                        "odd":  [1, 3, 5, 7],
                        "even": [2, 6, 8, 9],
                        "all":  [1, 2, 3, 5, 6, 7, 8, 9],
                    },
                    u"冬": {
                        "odd":  [11, 13, 15, 17],
                        "even": [12, 14, 16, 18],
                        "all":  [11, 12, 13, 14, 15, 16, 17, 18],
                    },
                    u"秋冬": {
                        "odd":  [1, 3, 5, 7, 11, 13, 15, 17],
                        "even": [2, 6, 8, 9, 12, 14, 16, 18],
                        "all":  [1, 2, 3, 5, 6, 7, 8, 9, 11, 12, 13, 14, 15, 16, 17, 18],
                    },
                }

                if u"单" in time_text:
                    odd_or_even = "odd"
                elif u"双" in time_text:
                    odd_or_even = "even"
                else:
                    odd_or_even = "all"

                weeks = week_data[semester_text][odd_or_even]

                number = re.findall("\d{1,2}", time_text[3:])
                lessons.append({
                    'day': chinese_week_numbers[time_text[1]],
                    'start': int(number[0]),
                    'end': int(number[-1]),
                    'weeks': weeks,
                })

            ''' - parse location'''
            locations = map(self.trim_location, locations)
            if len(locations) > 1:
                '''each lesson has different location'''
                for i in range(len(lessons)):
                    try:
                        lessons[i]['location'] = locations[i]
                    except IndexError:
                        # TODO: log
                        pass
            elif len(locations) == 1:
                '''lessons share the same location'''
                for l in lessons:
                    l['location'] = locations[0]

            '''deal w/ special case: one lesson separated to two'''
            lessons = sorted(lessons, key=lambda x: (x['day'], x['start']))
            for i in range(1, len(lessons)):
                if (lessons[i]['day'] == lessons[i - 1]['day'] and
                  lessons[i]['start'] == lessons[i - 1]['end'] + 1 and
                  lessons[i]['location'] == lessons[i - 1]['location']):
                    lessons[i - 1]['end'] = lessons[i]['end']
                    lessons[i]['delete'] = True
            lessons = filter(lambda x: 'delete' not in x, lessons)

            course = {
                'original_id': cols[0].get_text(strip=True),
                'name': cols[1].get_text(strip=True),
                'teacher': cols[2].get_text(strip=True),
                'lessons': lessons,
            }
            courses.append(course)
        pretty_print(courses)
        return soup.prettify().encode("utf8")

if __name__ == "__main__":
    grabber = TeapotParser()
    # grabber.test()
    grabber.grab_all()
