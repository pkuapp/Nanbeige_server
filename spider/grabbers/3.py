#! python
# -*- coding: utf-8 -*-

from django.http import HttpResponse
from django.utils import simplejson
from django.shortcuts import *
from types import *
from BeautifulSoup import *
import urllib,urllib2
import re
from nbg.models import *

user_agent = r'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'
urlroot = r'http://byjw.bupt.edu.cn:8080'
urlend = r''         
urlin = r"http://byjw.bupt.edu.cn:8080/jwLoginAction.do"
urlcourse = r"http://byjw.bupt.edu.cn:8080/xkAction.do?actionType=6"
urlout = r"http://byjw.bupt.edu.cn:8080/logout.do"

#info showed when logged in successfully
plogin = re.compile(u'学分制综合教务')

def _loginFromData(request,data):
	
    user = authenticate(username=data['username'],password=data['password'])
    if user is not None:
        if user.is_active:
                auth_login(request,user)
                return HttpResponse('0')
        else:
                return HttpResponse('-1')
    return HttpResponse('-9')

def login_urp_with_data(**kwarg):
    data = kwarg['data']
    JSESSIONID = kwarg['JSESSIONID']
    request = kwarg['request']
    headers = {'User-Agent': user_agent, 'Cookie': 'JSESSIONID='+JSESSIONID}

    if data['zjh'] == u'':
        return HttpResponse('-1')
    else:
        url_values = urllib.urlencode(data)
        #login
        req = urllib2.Request(urlin, url_values, headers)
        response = urllib2.urlopen(req)
        logindata = response.read().decode('gb18030')
        response.close()
        if re.search(plogin, logindata):
            #read course
            req = urllib2.Request(urlcourse, None, headers)
            response = urllib2.urlopen(req)
            coursedata = response.read().decode('gb18030')
            response.close()
            #logout
            req = urllib2.Request(urlout, None, headers)
            response = urllib2.urlopen(req)
            logoutdata = response.read().decode('gb18030')
            response.close()
            #deal with course data
            #return HttpResponse(coursedata)
            return HttpResponse(get_course(coursedata))
        else:
            return HttpResponse('login error')

def login(request):
    data = {}
    JSESSIONID = request.POST.get('sid', None)
    #add parameters that the login webpage needs here!
    data['type'] = 'sso'
    data['zjh'] = request.POST.get('zjh', None)
    data['mm'] = request.POST.get('mm', None)
    return login_urp_with_data(**locals())

def get_course(coursedata):
    table_soup = BeautifulSoup(coursedata)
    soup_course = table_soup.findAll('table', {'class':'displayTag', 'id':'user'})
    tablebody = str(soup_course[1])
    rows_soup = BeautifulSoup(tablebody)
    rows = rows_soup.findAll('tr',{'class':'odd'})
    courselist = list()
    for row in rows:
        td_soup = BeautifulSoup(str(row))
        tdbody = td_soup.findAll('td')
        courserow = {
            'fangan': tdbody[0].getText().strip('&nbsp'),
            'original_id': tdbody[1].getText().strip('&nbsp'),
            'name': tdbody[2].getText().strip('&nbsp'),
            'xuhao': tdbody[3].getText().strip('&nbsp'),
            'credit': tdbody[4].getText().strip('&nbsp'),
            'xuanxiuma': tdbody[5].getText().strip('&nbsp'),
            'kaochama': tdbody[6].getText().strip('&nbsp'),
            'teacher': tdbody[7].getText().strip('&nbsp'),
            'di ji zhou shang': tdbody[11].getText().strip('&nbsp'),
            'xingqi' : tdbody[12].getText().strip('&nbsp'),
            'jieci' : tdbody[13].getText().strip('&nbsp'),
            'jieshu': tdbody[14].getText().strip('&nbsp'),
            'xiaoqu': tdbody[15].getText().strip('&nbsp'),
            'building' : tdbody[16].getText().strip('&nbsp'),
            'jiaoshi' : tdbody[17].getText().strip('&nbsp'),
        }
        courselist.append(courserow)
        get_original_id = tdbody[1].getText().strip('&nbsp')
        get_course_name = tdbody[2].getText().strip('&nbsp')
        get_teacher_name = tdbody[7].getText().strip('&nbsp')
        get_credit = tdbody[4].getText().strip('&nbsp')
        get_weeks = tdbody[12].getText().strip('&nbsp')
        get_campus = tdbody[15].getText().strip('&nbsp')
        try:
            course_obj = Course.objects.get(original_id=get_original_id,name=get_course_name,teacher=get_teacher_name)
            get_location = tdbody[16].getText().strip('&nbsp') + ' ' + tdbody[17].getText().strip('&nbsp')
            if tdbody[12].getText().strip('&nbsp') != '' and tdbody[13].getText().strip('&nbsp') != '' and tdbody[14].getText().strip('&nbsp') != '':
                get_day = int(tdbody[12].getText().strip('&nbsp'))
                get_course_start = int(tdbody[13].getText().strip('&nbsp'))
                get_course_end = get_course_start + int(tdbody[14].getText().strip('&nbsp')) - 1
                course_lesson = Lesson.objects.filter(course=course_obj,day=get_day, start=get_course_start,end=get_course_end)
                current_user = request.user              
                if course_lesson.count() == 0:
                    course_new = add_course(get_course_name, get_original_id, get_credit, get_teacher_name, get_course_start, get_course_end, get_location, get_weeks)[0]
                    current_user.courses.add(course_new)
                else:
                    current_user.courses.add(course_obj)
        except:
                course_new = add_course(get_course_name, get_original_id, get_credit, get_teacher_name, get_course_start, get_course_end, get_location, get_weeks)[0]
                current_user.courses.add(course_new)
    return HttpResponse(simplejson.dumps(courselist))

def add_course(g_name, g_original_id, g_credit, g_teacher, g_day, g_start, g_end, g_location, g_weeks):
    course = Course(name=g_name, original_id=g_original_id, credit=g_credit, teacher=g_teacher)
    lesson = Lesson(day=g_day,start=g_start, end=g_end, location=g_location, course=course)
    course.save()
    lesson.save()
    return course, lesson