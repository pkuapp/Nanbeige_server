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
urlin = r"http://byjw.bupt.edu.cn:8080/jwLoginAction.do"
urlcourse = r"http://byjw.bupt.edu.cn:8080/xkAction.do?actionType=6"
urlout = r"http://byjw.bupt.edu.cn:8080/logout.do"

#info showed when logged in successfully
plogin = re.compile(u'学分制综合教务')

# def _loginFromData(request,data):
#     user = authenticate(username=data['username'],password=data['password'])
#     if user is not None:
#         if user.is_active:
#                 auth_login(request,user)
#                 return HttpResponse('0')
#         else:
#                 return HttpResponse('-1')
#     return HttpResponse('-9')

def login_urp(request):
    data = {}
    JSESSIONID = request.POST.get('sid', None)
    #add parameters that the login webpage needs here!
    data['type'] = 'sso'
    data['zjh'] = request.POST.get('zjh', None)
    data['mm'] = request.POST.get('mm', None)
    return read_urp_course_data(**locals())

def read_urp_course_data(**kwarg):
    data = kwarg['data']
    JSESSIONID = kwarg['JSESSIONID']
    request = kwarg['request']
    headers = {'User-Agent': user_agent, 'Cookie': 'JSESSIONID='+JSESSIONID}

    if data['zjh'] == u'' or data['mm'] == u'':
        return HttpResponse('student no. and password required')
    else:
        url_values = urllib.urlencode(data)
        try:
            #login
            req = urllib2.Request(urlin, url_values, headers)
            response = urllib2.urlopen(req)
            logindata = response.read().decode('gb18030')
            response.close()
            if re.search(plogin, logindata):
                #read course
                req = urllib2.Request(urlcourse, None, headers)
                response = urllib2.urlopen(req)
                doc_courses = response.read().decode('gb18030')
                response.close()
                #logout
                req = urllib2.Request(urlout, None, headers)
                response = urllib2.urlopen(req)
                response.close()
                #deal with course data
                return HttpResponse(parse_urp_doc_course(doc_courses,request))
            else:
                return HttpResponse('login error, password might be wrong')
        except Exception, e:
            return HttpResponse('network error')

def parse_urp_doc_course(doc,request):
    returnl=list()
    strainer= SoupStrainer('tr',{'class':'odd'})
    soup = BeautifulSoup(doc, parseOnlyThese=strainer)
    for row in soup:
        if type(row)==Tag:
            if row.td.has_key('rowspan'):
                rowspan = int(row.td['rowspan'])
                rowraw = list()
                for td in row:
                    if type(td) == Tag:
                        rowraw.append(td.getText().strip('&nbsp;'))
                oncourse = {
                    'name': rowraw[2],
                    'original_id': rowraw[1],
                    'credit': rowraw[4],
                    #'semester': Semester.objects.get(pk=1),
                    'teacher': rowraw[7],
                    'ta': '',
                    'lessons-numbers': rowspan,
                    'lessons':[{
                        'day': int(rowraw[12]),
                        'start': int(rowraw[13]),
                        'end': int(rowraw[13]) + int(rowraw[14]) -1,
                        'location': rowraw[16]+' '+rowraw[17],
                        'weeks': rowraw[11]
                    }]
                }
                #下面把这节课的多个上课时间取出（如果上课时间超过一个的话）
                if rowspan>1:
                    lessonrow=row.nextSibling
                    for i in xrange(rowspan-1):
                        if type(lessonrow)==Tag:
                            rowraw = list()
                            for td in lessonrow:
                                if type(td) == Tag:
                                    rowraw.append(td.getText().strip('&nbsp;')) 
                            onlesson = {
                                'day': int(rowraw[1]),
                                'start': int(rowraw[2]),
                                'end': int(rowraw[2]) + int(rowraw[3]) -1,
                                'location': rowraw[5]+' '+rowraw[6],
                                'weeks': rowraw[0]
                            }
                            oncourse['lessons'].append(onlesson)
                        lessonrow=lessonrow.nextSibling
                returnl.append(oncourse)
    return simplejson.dumps(returnl)


#以下几个函数暂时不用
def get_course(coursedata,request):
    table_soup = BeautifulSoup(coursedata)
    soup_course = table_soup.findAll('table', {'class':'displayTag', 'id':'user'})
    tablebody = str(soup_course[1])
    rows_soup = BeautifulSoup(tablebody)
    rows = rows_soup.findAll('tr',{'class':'odd'})
    courselist = list()
    for row in rows:
        td_soup = BeautifulSoup(str(row))
        tdbody = td_soup.findAll('td')
    #     courserow = {
    #         'fangan': tdbody[0].getText().strip('&nbsp'),
    #         'original_id': tdbody[1].getText().strip('&nbsp'),
    #         'name': tdbody[2].getText().strip('&nbsp'),
    #         'xuhao': tdbody[3].getText().strip('&nbsp'),
    #         'credit': tdbody[4].getText().strip('&nbsp'),
    #         'xuanxiuma': tdbody[5].getText().strip('&nbsp'),
    #         'kaochama': tdbody[6].getText().strip('&nbsp'),
    #         'teacher': tdbody[7].getText().strip('&nbsp'),
    #         'di ji zhou shang': tdbody[11].getText().strip('&nbsp'),
    #         'xingqi' : tdbody[12].getText().strip('&nbsp'),
    #         'jieci' : tdbody[13].getText().strip('&nbsp'),
    #         'jieshu': tdbody[14].getText().strip('&nbsp'),
    #         'xiaoqu': tdbody[15].getText().strip('&nbsp'),
    #         'building' : tdbody[16].getText().strip('&nbsp'),
    #         'jiaoshi' : tdbody[17].getText().strip('&nbsp'),
    #     }
    #     courselist.append(courserow)
        get_semester = Semester.objects.get(pk=1)
        get_original_id = tdbody[1].getText().strip('&nbsp;')
        get_course_name = tdbody[2].getText().strip('&nbsp;')
        get_teacher_name = tdbody[7].getText().strip('&nbsp;')
        get_credit = tdbody[4].getText().strip('&nbsp;')
        get_weeks = tdbody[12].getText().strip('&nbsp;')
        get_campus = tdbody[15].getText().strip('&nbsp;')
        get_location = tdbody[16].getText().strip('&nbsp') + ' ' + tdbody[17].getText().strip('&nbsp;')
        get_day = int(tdbody[12].getText().strip('&nbsp;'))
        get_course_start = int(tdbody[13].getText().strip('&nbsp;'))
        get_course_end = get_course_start + int(tdbody[14].getText().strip('&nbsp;')) - 1
        test_day = tdbody[12].getText().strip('&nbsp;')
        test_start = tdbody[13].getText().strip('&nbsp;')
        test_end = tdbody[14].getText().strip('&nbsp;')
        try:
            course_obj = Course.objects.get(original_id=get_original_id,name=get_course_name,teacher=get_teacher_name)
            if test_day != '' and test_start != '' and test_end != '':
                course_lesson = Lesson.objects.filter(course=course_obj,day=get_day, start=get_course_start,end=get_course_end)
                current_user = request.user              
                if course_lesson.count() == 0:
                    course_new = add_course(get_semester, get_course_name, get_original_id, get_credit, get_teacher_name,get_day, get_course_start, get_course_end, get_location, get_weeks)[0]
                    lesson_new = add_course(get_semester, get_course_name, get_original_id, get_credit, get_teacher_name,get_day, get_course_start, get_course_end, get_location, get_weeks)[1]
                    current_user.get_profile().courses.add(course_new)
                    consequence = show_result(get_semester, get_course_name, get_original_id, get_credit, get_teacher_name,get_day, get_course_start, get_course_end, get_location, get_weeks)                
                else:
                    current_user.get_profile().courses.add(course_obj)
        except:
            current_user = request.user
            course_new = add_course(get_semester, get_course_name, get_original_id, get_credit, get_teacher_name, get_day, get_course_start, get_course_end, get_location, get_weeks)[0]
            lesson_new = add_course(get_semester, get_course_name, get_original_id, get_credit, get_teacher_name,get_day, get_course_start, get_course_end, get_location, get_weeks)[1]
            current_user.get_profile().courses.add(course_new)
            consequence = show_result(get_semester, get_course_name, get_original_id, get_credit, get_teacher_name,get_day, get_course_start, get_course_end, get_location, get_weeks)
    return consequence

def add_course(g_semester, g_name, g_original_id, g_credit, g_teacher, g_day, g_start, g_end, g_location, g_weeks):
    course = Course(semester=g_semester , name=g_name, original_id=g_original_id, credit=g_credit, teacher=g_teacher)
    course.save()
    lesson = Lesson(day=g_day,start=g_start, end=g_end, location=g_location, course=course)
    lesson.save()
    return course, lesson

def show_result(g_semester, g_name, g_original_id, g_credit, g_teacher, g_day, g_start, g_end, g_location, g_weeks):
    course_objs = Course.objects.filter(semester=g_semester , name=g_name, original_id=g_original_id, credit=g_credit, teacher=g_teacher)
    response = [{
        'semester'  : course_item.semester,
        'course_name' : course_item.name,
        'credit' : course_item.credit,
        'original_id' : course_item.original_id,
        'teacher' : course_item.teacher,
        'lesson' : [
        {
            'day' : lesson_item.day,
            'start' : lesson_item.start,
            'end' : lesson_item.end,
            'location' : lesson_item.location,
        }for lesson_item in course_item.lesson_set.all()]
     }for course_item in course_objs]
    return response