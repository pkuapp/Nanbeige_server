#! python
# -*- coding: utf-8 -*-

from django.http import HttpResponse
from django.utils import simplejson
from django.shortcuts import *
from types import *
from BeautifulSoup import *
import urllib,urllib2
import re
from django.contrib.models import User
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

        else:
            return HttpResponse('login error')
        #if re.search(plogin,logindata.decode('gb18030')):
          #  '''get course data'''
            #req = urllib2.urlopen(req)

def login(request):
    data = {}
    JSESSIONID = request.POST.get('sid', None)
    #add parameters that the login webpage needs here!
    data['type'] = 'sso'
    data['zjh'] = request.POST.get('zjh', None)
    data['mm'] = request.POST.get('mm', None)
    return login_urp_with_data(**locals())

