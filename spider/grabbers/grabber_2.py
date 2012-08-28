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
    """Parser for Zhejiang University.
    """
    def __init__(self):
        super(TeapotParser, self).__init__()
        self.require_captcha = True
        self.available = True
        self.semester_id = 5
        self.url_prefix = "http://jwbinfosys.zju.edu.cn/"
        self.charset = "gbk"

        '''weekset data ONLY FOR SEMESTER 5, should be updated every semester
        '''
        self.week_data = {
            u"短": {
                "odd":  1,
                "even": 1,
                "all":  1,
            },
            u"秋": {
                "odd":  2,
                "even": 3,
                "all":  4,
            },
            u"冬": {
                "odd":  5,
                "even": 6,
                "all":  7,
            },
            u"秋冬": {
                "odd":  8,
                "even": 9,
                "all":  10,
            },
        }

    def get_semester_from_time(self, time_text):
        if u"秋冬" in time_text:
            return u"秋冬"
        elif u"秋" in time_text:
            return u"秋"
        elif u"冬" in time_text:
            return u"冬"
        else:
            return None

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
        except:
            raise
        else:
            with open(os.path.join(os.path.dirname(__file__), 'log.html'), 'w') as log:
                log.write(response)

    @staticmethod
    def parse_odd_or_even(text):
        if u"单" in text:
            return "odd"
        elif u"双" in text:
            return "even"
        else:
            return "all"

    @staticmethod
    def trim_location(l):
        l = l.replace(u"(多媒体，音乐教室)", "")
        l = l.replace(u"(科创专用教室)", "")
        l = l.replace(u"(网络五边语音)", "")
        l = l.replace(u"(网络五边菱)", "")
        l = l.replace(u"(长方无黑板)", "")
        l = l.replace(u"(五边菱形)", "")
        l = l.replace(u"(六边圆形)", "")
        l = l.replace(u"(网络六边)", "")
        l = l.replace(u"(网络五边)", "")
        l = l.replace(u"(传统语音)", "")
        l = l.replace(u"(长方形)", "")
        l = l.replace(u"(语音)", "")
        l = l.replace(u"(成多)", "")
        l = l.replace(u"(普)", "")
        l = l.replace(u"(多)", "")
        l = l.replace("*", "")
        return l

    def get_lessons(self, time_texts, locations, semester_text):
        '''parse lesson'''
        ''' - parse time'''
        lessons = []
        for time_text in time_texts:
            '''parse week'''
            odd_or_even = self.parse_odd_or_even(time_text)

            '''sometimes, lesson has its own semester text'''
            semester = self.get_semester_from_time(time_text)
            if semester:
                weekset_id = self.week_data[semester][odd_or_even]
            else:
                weekset_id = self.week_data[semester_text][odd_or_even]

            number = re.findall("\d{1,2}", time_text[3:])
            if time_text:
                weekday = re.search(u"周(.)", time_text).group(1)
                lessons.append({
                    'day': chinese_weekdays[weekday],
                    'start': int(number[0]),
                    'end': int(number[-1]),
                    'weekset_id': weekset_id,
                })
            else:
                lessons.append({})

        ''' - parse location'''
        locations = map(self.trim_location, locations)
        if len(locations) > 1:
            '''each lesson has different location'''
            for i in range(len(lessons)):
                if lessons[i]:
                    try:
                        lessons[i]['location'] = locations[i]
                    except IndexError:
                        # TODO: log
                        pass
        elif len(locations) == 1:
            '''lessons share the same location'''
            for l in lessons:
                if l:
                    l['location'] = locations[0]

        lessons = filter(bool, lessons)

        '''deal w/ special case: one lesson separated to two'''
        lessons = sorted(lessons, key=lambda x: (x['day'], x['start']))
        for i in range(1, len(lessons)):
            if (lessons[i]['day'] == lessons[i - 1]['day'] and
              lessons[i]['start'] == lessons[i - 1]['end'] + 1 and
              lessons[i]['location'] == lessons[i - 1]['location']):
                lessons[i - 1]['end'] = lessons[i]['end']
                lessons[i]['delete'] = True
        lessons = filter(lambda x: 'delete' not in x, lessons)

        return lessons


    def grab_all(self):
        # self._local_setup()
        # self._login()
        self._fake_login()

        url_courses = self.url_prefix + "jxrw_zd.aspx?xh=" + self.username

        '''get viewstate'''
        r_viewstate = requests.get(url_courses, cookies=self.cookies)
        result = re.search('<input type="hidden" name="__VIEWSTATE" value="(.+)" />', r_viewstate.content)
        viewstate = result.group(1)

        print "Get viewstate: done."

        '''parser, start.'''

        ''' - get colleges'''
        strainer_colleges = SoupStrainer("select", id="ddlXY")
        soup_colleges = BeautifulSoup(r_viewstate.content.decode(self.charset), parse_only=strainer_colleges)
        colleges = [option['value'] for option in soup_colleges.select("option") if option['value']]
        pretty_print(colleges)
        print "{} colleges.".format(len(colleges))

        ''' - iter colleges'''
        total_courses = 0
        for i, college in enumerate(colleges):
            '''get courses'''
            data = {
                '__EVENTTARGET': "",
                '__EVENTARGUMENT': "",
                '__VIEWSTATE': viewstate,
                'ddlXN': "2012-2013",
                'ddlXQ': "1",
                'ddlXY': college.encode(self.charset),
                'ddlZY': "",
                'ddlKC': "",
                'btnFilter': u' 查 询 '.encode(self.charset),
            }
            r_courses = requests.post(url_courses, data=data, cookies=self.cookies)
            content = r_courses.content.decode(self.charset)

            strainer_courses = SoupStrainer("table", id="DBGrid")
            soup_courses = BeautifulSoup(content, parse_only=strainer_courses)
            rows = soup_courses.select("tr")

            courses = []
            for r in rows:
                if r.has_key('class') and r['class'] == ["datagridhead"]:
                    continue

                cols = r.select("td")
                semester_text = cols[0].get_text(strip=True)
                teacher = cols[7].get_text(strip=True).replace('/', ',')
                time_texts = map(string.strip, cols[8].get_text().split(';'))
                locations = map(string.strip, cols[9].get_text().split(';'))

                lessons = self.get_lessons(time_texts, locations, semester_text)

                course = {
                    'original_id': cols[3].get_text(strip=True),
                    'name': cols[4].get_text(strip=True),
                    'credit': float(cols[6].get_text(strip=True)),
                    'teacher': teacher,
                    'lessons': lessons,
                }
                courses.append(course)

            print "#{} {}: {} courses.".format(i, college.encode("utf8"), len(courses))
            total_courses += len(courses)
            output_dir = os.path.join(os.path.dirname(__file__), 'zju')
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)
            with open(os.path.join(output_dir, str(i) + '.yaml'), 'w') as yaml_file:
                yaml_file.write(pretty_format(courses))
            # with open(os.path.join(output_dir, str(i) + '.html'), 'w') as html_file:
            #     html_file.write(soup_courses.prettify().encode("utf8"))
        print "Done! Totally exported {} courses.".format(total_courses)

    def _fake_login(self):
        self.username = "3110000420"
        self.cookies = {'ASP.NET_SessionId': "bn35e2epipm0xvewtjrzvw45"}

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
        if u"调查问卷".encode(self.charset) in r_course.content:
            raise GrabError("无法抓取您的课程，请先填写教务网调查问卷。")
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

            lessons = self.get_lessons(time_texts, locations, semester_text)

            course = {
                'original_id': cols[0].get_text(strip=True),
                'name': cols[1].get_text(strip=True),
                'teacher': cols[2].get_text(strip=True),
                'lessons': lessons,
            }
            courses.append(course)
        self.courses = courses
        return pretty_format(courses)

if __name__ == "__main__":
    grabber = TeapotParser()
    # grabber.test()
    grabber.grab_all()
