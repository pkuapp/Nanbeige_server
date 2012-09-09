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
        self.week_data = {
            '教学周：第 1-3、7-19 周': '1,2,3,7,8,9,10,11,12,13,14,15,16,17,18,19',
            '实践教学：第1周': '1',
            '4,6,8-9,12,14-15,18周上': '4,6,8,9,12,14,15,18',
            '3,9,13,17周上': '3,9,13,17',
            '4,7,11,15周上': '4,7,11,15',
            '实践教学：第1-2周': '1,2',
            '10-17周上': '10,11,12,13,14,15,16,17',
            '教学周：第 12-19 周': '12,13,14,15,16,17,18,19',
            '8-15周上': '8,9,10,11,12,13,14,15',
            '10-13周上': '10,11,12,13',
            '教学周：第 4-19 周': '4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19',
            '教学周：第 8-11 周': '8,9,10,11',
            '1-3，7-19周（双周）': '1,2,3,8,10,12,14,16,18',
            '9-16周上': '9,10,11,12,13,14,15,16',
            '7-14周上': '7,8,9,10,11,12,13,14',
            '4-5,10-19周上': '4,5,10,11,12,13,14,15,16,17,18,19',
            '3,5,9,14周上': '3,5,9,14',
            '5,8,12,15周上': '5,8,12,15',
            '16周上': '16',
            '4-15周上': '4,5,6,7,8,9,10,11,12,13,14,15',
            '8-9,14-15周上': '8,9,14,15',
            '4-16周上': '4,5,6,7,8,9,10,11,12,13,14,15,16',
            '3,10,16-17周上': '3,10,16,17',
            '教学周：第 4-19 周（单周）': '5,7,9,11,13,15,17,19',
            '3,7,11,15周上': '3,7,11,15',
            '4-15,17-19周上': '4,5,6,7,8,9,10,11,12,13,14,15,17,18,19',
            '1-16周上': '1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16',
            '教学周：第 4-19 周（双周）': '4,6,8,10,12,14,16,18',
            '实践教学：第2周': '2',
            '5-12周上': '5,6,7,8,9,10,11,12',
            '5,9,13,17周上': '5,9,13,17',
            '教学周：第 12-15 周': '12,13,14,15',
            '17周上': '17',
            '实践教学：第1-3周': '1,2,3',
            '4-9周上': '4,5,6,7,8,9',
            '教学周：第 4-17 周': '4,5,6,7,8,9,10,11,12,13,14,15,16,17',
            '教学周：第 4-17 周（双周）': '4,6,8,10,12,14,16',
            '14-17周上': '14,15,16,17',
            '教学周：第 4-11 周': '4,5,6,7,8,9,10,11',
            '4,8,12,16周上': '4,8,12,16',
            '5-6,9-10,13-14,17-19周上': '5,6,9,10,13,14,17,18,19',
            '4,7,11,14周上': '4,7,11,14',
            '教学周：第 16-19 周': '16,17,18,19',
            '5,9,14周上': '5,9,14',
            '实践教学：第2-3周': '2,3',
            '': 'None',
            '实践教学：第3周': '3',
            '教学周：第 4-17 周（单周）': '5,7,9,11,13,15,17',
            '1-3，7-19周（单周）': '1,2,3,7,9,11,13,15,17,19',
            '4-5,10-11周上': '4,5,10,11',
            '10-12周上': '10,11,12',
            '10,12,14周上': '10,12,14',
            '13-15周上': '13,14,15',
            '9,11,13周上': '9,11,13',
        }

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

    def get_lessons(self, week_text, day_text, start_end_text, location):
        lessons = []

        if location == '  ':
            location = None
        if day_text == '':
            day_text = None
        else:
            day_text = int(day_text)

        weeks = []
        slices = week_text.split(',')
        if slices[0] == week_text:
            slices = week_text.split(u'、')
        if slices[0] == week_text:
            slices = week_text.split(u'，')
        for mouse in slices:
            res = []
            baidu = re.search('\d+-\d+', mouse)
            if baidu:
                data = re.findall('\d+', baidu.group(0))
                res = [i for i in range(int(data[0]), int(data[1]) + 1)]
            else:
                google = re.search('\d+', mouse)
                if google:
                    data = re.findall('\d+', google.group(0))
                    res = [int(data[0])]
            if u'单周' in mouse:
                res = [i for i in res if i % 2 == 1]
            elif u'双周' in mouse:
                res = [i for i in res if i % 2 == 0]
            weeks.extend(res)

        weeks.sort()
        weeks = list_to_comma_separated(weeks)
        if weeks == '':
            weeks = 'None'

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
            'weeks': list_to_comma_separated(weeks),
            'week_raw': week_text,
            'location': location,
        })

        return lessons

    def get_teachers(self, teachers_text):
        return teachers_text.replace('* ', ',').rstrip(',').rstrip('*').replace(' ', ',')

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
        print "{} colleges.".format(len(colleges))

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
                week_text = cols[4].get_text(strip=True)
                day_text = cols[5].get_text(strip=True)
                start_end_text = cols[6].get_text(strip=True)
                location = cols[7].get_text(strip=True) + ' ' + cols[8].get_text(strip=True) + ' ' + cols[9].get_text(strip=True)
                lessons = self.get_lessons(week_text, day_text, start_end_text, location)
                code_name = cols[10].get_text(strip=True)

                course = {
                    'original_id': cols[0].get_text(strip=True),
                    'name': cols[1].get_text(strip=True),
                    'credit': float(cols[2].get_text(strip=True).replace('&nbsp;', '')),
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

            print "#{} {}: {} courses.".format(i, college.encode("utf8"), len(courses))
            total_courses += len(courses)
            output_dir = os.path.join(os.path.dirname(__file__), 'bupt')
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)
            if courses != []:
                with open(os.path.join(output_dir, str(i) + '.yaml'), 'w') as yaml_file:
                    yaml_file.write(pretty_format(courses))
        print "Done! Totally exported {} courses.".format(total_courses)

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
            week_text = cols[11].get_text(strip=True)
            day_text = cols[12].get_text(strip=True)
            start_end_text = cols[13].get_text(strip=True) + '-' + str(int(cols[13].get_text(strip=True)) + int(cols[14].get_text(strip=True)))
            
            lessons = self.get_lessons(week_text, day_text, start_end_text, location)

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
