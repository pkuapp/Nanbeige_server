#!/usr/bin/env python
# -*- coding: utf-8 -*-

import csv
import re
from helpers import pretty_format, list_to_comma_separated


#import pdb; pdb.set_trace()

def get_teachers(teachers_text):
    return teachers_text.replace('* ', ',').rstrip(',').rstrip('*').replace(' ', ',').rstrip(',')

def get_lesson(weeks_text, day_text, start_end_text, location):
    if location == '  ':
        location = None

    if day_text == '':
        day_text = None
    else:
        day_text = int(day_text)

    # week_num = re.findall("\d{1,2}", week_text)
    # try:
    #     weeks = [i for i in range(int(week_num[0]), int(week_num[1]) + 1)]
    # except:
    #     weeks = []
    # try:
    #     weeks = weeks + [i for i in range(int(week_num[2]), int(week_num[3]) + 1)]
    # except:
    #     pass
    # if weeks == []:
    #     if week_num == []:
    #         weeks = None
    #     else:
    #         weeks = [week_num[0]]
    #         weeks = list_to_comma_separated(weeks)

    # weeks = []

    # week_num = week_text.split(',')
    # for col in week_num:
    #     wkno = re.findall("\d{1,2}", col)
    #     print wkno
    #     if len(wkno) == 2:
    #         weeks = weeks + range(int(wkno[0]), int(wkno[1]) + 1)
    #     else:
    #         weeks.append(wkno[0])

    # weeks = list_to_comma_separated(weeks)

    weeks = []
    weeks_show = '第'

    for col in week_text.split(','):
        if not col:
            pass
        elif '-' in col:
            tmp = re.findall("\d{1,2}", str(re.findall("\d{1,2}-\d{1,2}", col)))
            weeks += range(int(tmp[0]), int(tmp[1]) + 1)
            weeks_show += tmp[0] + '-' + tmp[1] + ' '
        else:
            wkno = re.findall("\d{1,2}", col)
            if not wkno:
                pass
            elif len(wkno) == 1:
                weeks.append(int(wkno[0]))
                weeks_show += wkno[0] + ' '
            else:
                print week_text
                raise AssertionError

    weeks_show = weeks_show.rstrip()
    weeks_show += '周'
    weeks = list_to_comma_separated(weeks)

    number = re.findall("\d{1,2}", start_end_text)
    if number == []:
        number = [None, None]
    else:
        number[0] = int(number[0])

    if not day_text or not start_end_text or not week_text:
        return None

    lesson = {
        'day': day_text,
        'start': number[0],
        'end': number[0],
        'weeks': weeks,
        'weeks_raw': weeks_text,
        'weeks_display': weeks_show,
        'location': location,
    }

    return lesson

try:
    with open('data/bjtu.csv') as src:
        source = csv.reader(src)
        source.next()

        prev_code_name = '-1'

        courses = []
        for row in source:
            try:
                test = row[0]
            except:
                break
            teacher = get_teachers(row[6])
            week_text = row[7]
            day_text = row[8]
            start_text = row[9]
            location = ''
            for i in range(10, 13):
                if not row[i]:
                    pass
                else:
                    location += ' ' + row[i]
            location = location.lstrip()

            lesson = get_lesson(week_text, day_text, start_text, location)
            code_name = row[3]

            course = {
                'original_id': row[1],
                'name': row[2],
                'credit': row[4],
                'teacher': teacher,
                'lessons': [lesson],
            }

            if courses:
                if (course['original_id'] == courses[-1]['original_id']
                  and course['teacher'] == courses[-1]['teacher']
                  and prev_code_name == code_name):
                    courses[-1]['lessons'].append(lesson)
                else:
                    courses.append(course)
            else:
                courses.append(course)

            prev_code_name = code_name

        #print courses
        total_courses = len(courses)
        print "Converted %d courses. Writing to yaml...\n" % total_courses
        if courses != []:
            with open(('bjtu.yaml'), 'w') as yaml_file:
                yaml_file.write(pretty_format(courses))

except IOError:
    print "Cannot open data/bjtu.csv, exiting."
    exit()
