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
        self.require_captcha = False
        self.available = True
        self.semester_id = 3
        self.url_prefix = "http://byjw.bupt.edu.cn:8080/"
        self.charset = "gbk"

    def _local_setup(self):
        # username = raw_input("Username: ")
        # password = getpass.getpass('Password: ')
        username = '09210364'
        password = 'Whc910131'
        self.setUp(username=username, password=password)

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

    def get_lessons(self, weeks_text, day_text, start_end_text, location):
        lessons = []

        if location == '  ':
            location = None
        if day_text == '':
            day_text = None
        else:
            day_text = int(day_text)

        weeks = []
        weeks_display = u'第'
        slices = weeks_text.split(',')
        if slices[0] == weeks_text:
            slices = weeks_text.split(u'、')
        if slices[0] == weeks_text:
            slices = weeks_text.split(u'，')
        for mouse in slices:
            res = []
            baidu = re.search('\d+-\d+', mouse)
            if baidu:
                data = re.findall('\d+', baidu.group(0))
                res = [i for i in range(int(data[0]), int(data[1]) + 1)]
                weeks_display = weeks_display + '{0}-{1}'.format(data[0], data[1])
                if u'单周' in mouse:
                    pos = weeks_display.rfind(u' ')
                    if pos != -1:
                        weeks_display = weeks_display[:pos] + u'周 '
                        weeks_display = weeks_display + u'第{0}-{1}'.format(data[0], data[1])
                    weeks_display = weeks_display + u'单周'
                    res = [i for i in res if i % 2 == 1]
                elif u'双周' in mouse:
                    pos = weeks_display.rfind(u' ')
                    if pos != -1:
                        weeks_display = weeks_display[:pos] + u'周 '
                        weeks_display = weeks_display + u'第{0}-{1}'.format(data[0], data[1])
                    weeks_display = weeks_display + u'双周'
                    res = [i for i in res if i % 2 == 0]
            else:
                google = re.search('\d+', mouse)
                if google:
                    data = re.findall('\d+', google.group(0))
                    res = [int(data[0])]
                    weeks_display = weeks_display + '{0}'.format(data[0])
            weeks.extend(res)
            weeks_display = weeks_display + ' '
        weeks_display = weeks_display[:-1]
        if weeks_display[-1] != u'周':
            weeks_display = weeks_display + u'周'
        weeks.sort()
        weeks = list_to_comma_separated(weeks)
        if weeks == '':
            weeks = 'None'
            weeks_display = ''

        number = re.findall("\d{1,2}", start_end_text)
        if number == []:
            number = [None, None]
        else:
            number[0] = int(number[0])
            number[1] = int(number[1])

        lessons.append({
            'day': day_text,
            'start': number[0],
            'end': number[1],
            'weeks': weeks,
            'weeks_raw': weeks_text,
            'weeks_display': weeks_display,
            'location': location,
        })

        return lessons

    def get_teachers(self, teachers_text):
        return teachers_text.replace('  ', ' ').replace('* ', ',').rstrip(',').rstrip('*').replace(' ', ',')

    def grab_all(self):
        self._local_setup()
        self._login()

        url_courses = self.url_prefix + 'courseSearchAction.do?temp=1'

        '''get TOKEN'''
        r_viewstate = requests.get(url_courses, cookies=self.cookies)
        result = re.search('<input type="hidden" name="org.apache.struts.taglib.html.TOKEN" value="(.+)">', r_viewstate.content)
        TOKEN = result.group(1)

        print "Get TOKEN: done."

        '''parser, start.'''

        ''' - get colleges'''
        strainer_colleges = SoupStrainer('select', id="xsjc")
        soup_colleges = BeautifulSoup(r_viewstate.content.decode('gbk').replace('name', 'id'), parse_only=strainer_colleges)
        colleges = [option['value'] for option in soup_colleges.select("option") if option['value']]
        pretty_print(colleges)
        print "{0} colleges.".format(len(colleges))

        ''' - iter colleges'''
        url_courses = self.url_prefix + 'courseSearchAction.do'
        total_courses = 0
        for i, college in enumerate(colleges):
            '''get courses'''
            showColumn = [u'kch#课程号'.encode('gbk'), u'kcm#课程名'.encode('gbk'), u'xf#学分'.encode('gbk'), u'skjs#教师'.encode('gbk'), u'zcsm#周次'.encode('gbk'), u'skxq#星期'.encode('gbk'), u'skjc#节次'.encode('gbk'), u'xqm#校区'.encode('gbk'), u'jxlm#教学楼'.encode('gbk'), u'jasm#教室'.encode('gbk'), u'kxh#课序号'.encode('gbk')]
            data = {
                'org.apache.struts.taglib.html.TOKEN': TOKEN.encode('gbk'),
                'pageNumber': "0".encode('gbk'),
                'actionType': "1".encode('gbk'),
                'xsjc': college.encode('gbk'),
                'pageSize': '1000'.encode('gbk'),
                'showColumn': showColumn,
            }
            r_courses = requests.post(url_courses, data=data, cookies=self.cookies)
            content = r_courses.content.decode('gbk')

            strainer_courses = SoupStrainer("table", id="titleTop2")
            soup_courses = BeautifulSoup(content.replace('class', 'id'), parse_only=strainer_courses)
            rows = soup_courses.select("tr")
            prev_code_name = '-1'

            courses = []
            for r in rows:
                if not r.has_key('id'):
                    continue

                cols = r.select("td")
                try:
                    test_text = cols[0].get_text(strip=True)
                except:
                    break
                teacher = self.get_teachers(cols[3].get_text(strip=True))
                weeks_text = cols[4].get_text(strip=True)
                day_text = cols[5].get_text(strip=True)
                start_end_text = cols[6].get_text(strip=True)
                location = cols[7].get_text(strip=True) + ' ' + cols[8].get_text(strip=True) + ' ' + cols[9].get_text(strip=True)
                lessons = self.get_lessons(weeks_text, day_text, start_end_text, location)
                code_name = cols[10].get_text(strip=True)

                course = {
                    'original_id': cols[0].get_text(strip=True),
                    'name': cols[1].get_text(strip=True),
                    'credit': str(float(cols[2].get_text(strip=True).replace('&nbsp;', ''))),
                    'teacher': teacher,
                    'lessons': lessons,
                }

                try:
                    last_course = courses.pop()
                except:
                    pass
                else:
                    if course['original_id'] == last_course['original_id'] and course['teacher'] == last_course['teacher'] and prev_code_name == code_name:
                        course['lessons'] = course['lessons'] + last_course['lessons']
                    else:
                        courses.append(last_course)

                prev_code_name = code_name
                courses.append(course)

            print "#{0} {1}: {2} courses.".format(i, college.encode("utf8"), len(courses))
            total_courses += len(courses)
            output_dir = os.path.join(os.path.dirname(__file__), 'bupt')
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)
            if courses != []:
                with open(os.path.join(output_dir, str(i) + '.yaml'), 'w') as yaml_file:
                    yaml_file.write(pretty_format(courses))
        print "Done! Totally exported {0} courses.".format(total_courses)

    def _login(self):
        url_login = self.url_prefix + 'jwLoginAction.do'
        data = {
            'type': 'sso',
            'zjh': self.username,
            'mm': self.password,
        }
        r_login = requests.post(url_login, data=data)

        content = r_login.content.decode('gbk')

        if 'frameset' not in content:
            raise LoginError("unknown")

        '''logged in successfully'''
        print "Logged in successfully."
        self.cookies = r_login.cookies

    def run(self):
        self._login()

        url_course = self.url_prefix + 'xkAction.do?actionType=6'
        r_course = requests.get(url_course, cookies=self.cookies)

        soup = BeautifulSoup(r_course.content.replace('class', 'id'))
        soup.prettify()
        soup = soup.find_all("table")[7]

        rows = soup.select("tr")

        courses = []
        for r in rows:
            if r.has_key('id') and r['id'] != "odd":
                continue

            cols = r.select("td")

            if cols == []:
                continue

            location = cols[15].get_text(strip=True) + ' ' + cols[16].get_text(strip=True) + ' ' + cols[17].get_text(strip=True)
            teacher = self.get_teachers(cols[7].get_text(strip=True))
            weeks_text = cols[11].get_text(strip=True)
            day_text = cols[12].get_text(strip=True)
            start_end_text = cols[13].get_text(strip=True) + '-' + str(int(cols[13].get_text(strip=True)) + int(cols[14].get_text(strip=True)))
            
            lessons = self.get_lessons(weeks_text, day_text, start_end_text, location)

            course = {
                'original_id': cols[1].get_text(strip=True),
                'name': cols[2].get_text(strip=True),
                'teacher': teacher,
                'lessons': lessons,
            }
            courses.append(course)

        self.courses = courses
        return pretty_format(courses)

if __name__ == "__main__":
    grabber = TeapotParser()
    #grabber.test()
    grabber.grab_all()
