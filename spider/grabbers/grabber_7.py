#!/usr/bin/env python
# -*- coding: utf-8 -*-

import csv
import re
from helpers import pretty_format, list_to_comma_separated

def get_teachers(teachers_text):
    return teachers_text.replace('* ', ',').rstrip(',').rstrip('*').replace(' ', ',')

def get_lesson(weeks_text, day_text, start_end_text, location):
    if location == '  ':
        location = None

    if day_text == '':
        day_text = None
    else:
        day_text = int(day_text)

    week_num = re.findall("\d{1,2}", weeks_text)
    try:
        weeks = [i for i in range(int(week_num[0]), int(week_num[1]) + 1)]
    except:
        weeks = []
    try:
        weeks = weeks + [i for i in range(int(week_num[2]), int(week_num[3]) + 1)]
    except:
        pass
    if weeks == []:
        if week_num == []:
            weeks = None
        else:
            weeks = [week_num[0]]
            weeks = list_to_comma_separated(weeks)

    number = re.findall("\d{1,2}", start_end_text)
    if number == []:
        number = [None, None]
    else:
        number[0] = int(number[0])

    lesson = {
        'day': day_text,
        'start': number[0],
        'end': number[0],
        'weeks': weeks,
        'weeks_raw': weeks_text,
        'location': location,
    }

    return lesson

source = csv.reader(open('data/bjtu.csv'))
source.next()

prev_code_name = '-1'

courses = []
for row in source:
    try:
        test = row[0]
    except:
        break
    teacher = get_teachers(row[6])
    weeks_text = row[7]
    day_text = row[8]
    start_text = row[9]
    location = row[10] + ' ' + row[11] + ' ' + row[12]
    lesson = get_lesson(weeks_text, day_text, start_text, location)
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

# print courses
total_courses = len(courses)
if courses:
    with open(('bjtu.yaml'), 'w') as yaml_file:
        yaml_file.write(pretty_format(courses))