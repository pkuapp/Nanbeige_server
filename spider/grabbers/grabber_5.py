#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import os.path
import re
import string
import getpass
from bs4 import BeautifulSoup, SoupStrainer
from helpers import pretty_print, pretty_format, chinese_weekdays, list_to_comma_separated
from grabber_base import BaseParser, LoginError

class TeapotParser(BaseParser):
    """Parser for Renmin University of China.
    """
    def __init__(self):
        super(TeapotParser, self).__init__()
        self.require_captcha = True
        self.available = True
        self.semester_id = 7
        self.url_prefix = "http://portal.ruc.edu.cn/"
        self.url_prefix_s = "https://portal.ruc.edu.cn/"
        self.charset = "gbk"

    def _fetch_img(self):
        url_captcha = self.url_prefix_s + "cas/Captcha.jpg"
        r = requests.get(url_captcha, verify=False)
        self.captcha_img = r.content
        self.cookies = r.cookies

    def _local_setup(self):
        self._fetch_img()
        with open(os.path.join(os.path.dirname(__file__), 'img.jpg'), 'w') as img:
            img.write(self.captcha_img)

        captcha = raw_input("Captcha: ")
        # username = raw_input("Username: ")
        # password = getpass.getpass('Password: ')
        username = '2009201243'
        password = 'alleluia_11'

        self.setUp(username=username, password=password, captcha=captcha)

    def test(self):
        try:
            response = self.run()
        except LoginError as e:
            print e.error
        else:
            with open(os.path.join(os.path.dirname(__file__), 'log.html'), 'w') as log:
                log.write(response)

    def get_lessons(self, time_and_location_texts):
        lessons = []

        for i in range(0, len(time_and_location_texts) / 3):
            j = i * 3
            week_num = re.findall("\d{1,2}", str(time_and_location_texts[j]))
            weeks = [i for i in range(int(week_num[1]), int(week_num[2]) + 1)]
            weekday = re.search("星期(.+),", str(time_and_location_texts[j+1])).group(1)
            number = re.findall("\d{1,2}", str(time_and_location_texts[j+1]))
            location = str(time_and_location_texts[j+2]).replace('<tagbr>　', '')
            location = location.replace('</tagbr>', '')
            location = location.replace(',', ' ')
            weeks_display_text = str(time_and_location_texts[j]).decode('utf8')
            weeks_raw = weeks_display_text[weeks_display_text.find(u'：')+1:weeks_display_text.find(u' ')].replace(u'～', u'-')
            weeks_display = re.sub(r'0([0-9])', r'\1', weeks_raw)
            lessons.append({
                'day': chinese_weekdays[weekday.decode('utf8')],
                'start': int(number[0]),
                'end': int(number[-1]),
                'weeks': list_to_comma_separated(weeks),
                'weeks_display': weeks_display,
                'weeks_raw': weeks_raw,
                'location': location,
            })

        return lessons

    def grab_all(self):
        self._local_setup()
        self.next_url = 'http://portal.ruc.edu.cn/cas/login?service=http%3A%2F%2Fportal.ruc.edu.cn%2Fidc%2Feducation%2Fselectcourses%2Fresultquery%2FResultQueryAction.do%3Fmethod%3DforwardAllQueryXkjg'
        self._login()

        r_cookies = requests.post(self.next_url, cookies=self.cookies, verify=False)
        content = r_cookies.content.decode(self.charset)
        self.cookies = r_cookies.cookies

        '''parser, start.'''

        ''' - get colleges'''
        strainer_colleges = SoupStrainer("select", id="condition_yx")
        soup_colleges = BeautifulSoup(r_cookies.content.decode('gbk'), parse_only=strainer_colleges)
        colleges = [option['value'] for option in soup_colleges.select("option") if option['value']]
        colleges_name = [option.get_text() for option in soup_colleges.select("option") if option['value']]
        pretty_print(colleges_name)
        print "{0} colleges.".format(len(colleges))

        ''' - iter colleges'''
        total_courses = 0
        for i, college in enumerate(colleges):
            '''get courses'''
            data = {
                'method': "allJxb",
                'condition_xnd': "2012-2013",
                'condition_xq': "1",
                'condition_yx': college.encode('gbk'),
                'isNeedInitSQL': "true",
            }
            url_courses = 'http://portal.ruc.edu.cn/idc/education/selectcourses/resultquery/ResultQueryAction.do'
            r_courses = requests.post(url_courses, data=data, cookies=self.cookies)
            content = r_courses.content.decode('gbk')

            soup_courses = BeautifulSoup(content)
            rows = soup_courses.find_all("row")

            if len(rows) == 1:
                print "#{0} {1}: {2} courses.".format(i, colleges_name[i].encode('utf8'), 0)
                continue

            courses = []
            for r in rows:
                teacher = r.select("xm")[0].get_text(strip=True).replace('/', ',')
                time_and_location_texts = r.select("sksj > tagbr")

                lessons = self.get_lessons(time_and_location_texts)

                course = {
                    'original_id': r.select("jxbh")[0].get_text(strip=True),
                    'name': r.select("kcmc")[0].get_text(strip=True),
                    'credit': str(float(r.select("xf")[0].get_text(strip=True))),
                    'teacher': teacher,
                    'lessons': lessons,
                }
                courses.append(course)

            print "#{0} {1}: {2} courses.".format(i, colleges_name[i].encode('utf8'), len(courses))
            total_courses += len(courses)
            output_dir = os.path.join(os.path.dirname(__file__), 'ruc')
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)
            if courses != []:
                with open(os.path.join(output_dir, colleges_name[i] + '.yaml'), 'w') as yaml_file:
                    yaml_file.write(pretty_format(courses))
        print "Done! Totally exported {0} courses.".format(total_courses)

    def _login(self):
        url_login = self.next_url

        page_login = requests.get(url_login, cookies=self.cookies, verify=False)
        result = re.search(u'<input type="hidden" name="lt" value="(.+)" />', page_login.content)
        self.lt = result.group(1)

        data = {
            'action': 'DCPLogin',
            'username': self.username,
            'password': self.password,
            'captcha': self.captcha,
            'lt': self.lt,
            'userNameType': 'cardID',
        }
        r_login = requests.post(url_login, data=data, cookies=self.cookies, verify=False)

        content = r_login.content.decode(self.charset)
        result = re.match(u'<div class="error">(.+)</div>', content)
        if result:
            msg = result.group(1).decode(self.charset)
            raise LoginError(msg)

        self.next_url = re.search(u'window.location.href="(.+)";', content).group(1)

        '''logged in successfully'''
        print "Logged in successfully."
        self.cookies = r_login.cookies

    def run(self):
        self.next_url = 'http://portal.ruc.edu.cn/cas/login?service=http%3A%2F%2Fportal.ruc.edu.cn%2Fidc%2Feducation%2Fselectcourses%2Fschedulequery%2FScheduleQueryAction.do%3Fmethod%3DstudentSchedule'
        self._login()

        url_course = self.next_url
        data = {
            'method': 'studentSchedule',
            'condition_xh': self.username,
            'condition_xnd': '2012-2013',
            'condition_xq': '1',
        }
        r_course = requests.get(url_course, data=data, cookies=self.cookies)
        print r_course.content.decode('gbk')

        print "Grabbed successfully."

if __name__ == "__main__":
    grabber = TeapotParser()
    # grabber.test()
    grabber.grab_all()
