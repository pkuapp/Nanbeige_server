
# -*- coding: utf-8 -*-

import os
import yaml
import csv
import re
from helpers import pretty_print, pretty_format, chinese_weekdays, list_to_comma_separated

def get_teachers(teachers_text):
    return teachers_text.replace('* ', ',').rstrip(',').rstrip('*').replace(' ', ',')

def get_lessons(week_text, day_text, start_end_text, location):
    lessons = []

    if location == '  ':
        location = None

    if day_text == '':
        day_text = None
    else:
        day_text = int(day_text)

    week_num = re.findall("\d{1,2}", week_text)
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

    lessons.append({
        'day': day_text,
        'start': number[0],
        'end': number[0],
        'weeks': weeks,
        'weeks_raw': week_text,
        'location': location,
    })

    return lessons

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
	week_text = row[7]
	day_text = row[8]
	start_text = row[9]
	location = row[10] + ' ' + row[11] + ' ' + row[12]
	lessons = get_lessons(week_text, day_text, start_text, location)
	code_name = row[3]

	course = {
		'original_id': row[1],
		'name': row[2],
		'credit': row[4],
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

#print courses
total_courses = len(courses)
if courses != []:
    with open(('bjtu.yaml'), 'w') as yaml_file:
        yaml_file.write(pretty_format(courses))