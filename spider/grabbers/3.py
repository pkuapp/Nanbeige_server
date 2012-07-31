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

def get_course(request):
    doc = """




<html lang="zh-CN">
<head>
<title>学生选课结果</title>


<meta http-equiv="Content-Type" content="text/html; charset=GBK">
<link href="/css/newcss/project.css" rel="stylesheet" type="text/css">

</head>
<body topmargin="0" leftmargin="0" rightmargin="0" style="overflow:auto;">










<table width="100%" border="0" align="center" cellpadding="0" cellspacing="0">
<tr><td class="Linetop"></td>
</tr>
</table>
<table width="100%"  border="0" cellpadding="0" cellspacing="0" class="title" id="tblHead">
 <tr>
  <td>
   <table border="0" width="100%" cellpadding="0" cellspacing="0" >
   <tr>
   <td width="50%" align="left" valign="middle">&nbsp;<b>选课结果(已安排时间地点)</b>&nbsp;</td>

<td width="50%" align="right">

2012年07月31日12时04分

</td>
</tr>
   </table>
  </tr>
</table>
<table width="100%" border="0" align="center" cellpadding="0" cellspacing="0"  >
 <tr>
  <td class="Linetop"></td>
 </tr>
</table>









<link href="/css/newcss/project.css" rel="stylesheet" type="text/css">






    <table width="100%" border="0" cellpadding="0" cellspacing="0" class="titleTop2">
         <tr>
          <td class="pageAlign">
           <table cellpadding="0" width="100%" class="displayTag" cellspacing="1" border="0" id="user">
                <tr>
    <td colspan="2" class="sortable">&nbsp;</td>


    <td width="13%" class="sortable">
    <div align="center">
    
            星期一
            
    </div>
    </td>

    <td width="13%" class="sortable">
    <div align="center">
    
            星期二
            
    </div>
    </td>

    <td width="13%" class="sortable">
    <div align="center">
    
            星期三
            
    </div>
    </td>

    <td width="13%" class="sortable">
    <div align="center">
    
            星期四
            
    </div>
    </td>

    <td width="13%" class="sortable">
    <div align="center">
    
            星期五
            
    </div>
    </td>

    <td width="13%" class="sortable">
    <div align="center">
    
            星期六
            
    </div>
    </td>

    <td width="13%" class="sortable">
    <div align="center">
    
            星期日
            
    </div>
    </td>

</tr>






<tr bgcolor="#FFFFFF">

<td width="3%" rowspan="4">&nbsp;<p class="style4">上午</p></td>


              <td width="11%">第1节(08:00-08:50)</td>
             
  
    <td>&nbsp;

     英语中级口语1_01(校本部教三楼3-428)<br>

</td>

    <td>&nbsp;

     英语泛读3_01(校本部教三楼3-426)<br>

</td>

    <td>&nbsp;

&nbsp;

</td>

    <td>&nbsp;

&nbsp;

</td>

    <td>&nbsp;

&nbsp;

</td>

    <td>&nbsp;

&nbsp;

</td>

    <td>&nbsp;

&nbsp;

</td>

  </tr>

<tr bgcolor="#FFFFFF">


              <td width="11%">第2节(09:00-09:50)</td>
             
  
    <td>&nbsp;

     英语中级口语1_01(校本部教三楼3-428)<br>

</td>

    <td>&nbsp;

     英语泛读3_01(校本部教三楼3-426)<br>

</td>

    <td>&nbsp;

&nbsp;

</td>

    <td>&nbsp;

&nbsp;

</td>

    <td>&nbsp;

&nbsp;

</td>

    <td>&nbsp;

&nbsp;

</td>

    <td>&nbsp;

&nbsp;

</td>

  </tr>

<tr bgcolor="#FFFFFF">


              <td width="11%">第3节(10:10-11:00)</td>
             
  
    <td>&nbsp;

&nbsp;

</td>

    <td>&nbsp;

&nbsp;

</td>

    <td>&nbsp;

&nbsp;

</td>

    <td>&nbsp;

     基础英语3_01(校本部教三楼3-326)<br>

</td>

    <td>&nbsp;

     汉语阅读与写作_01(校本部教三楼3-417)<br>

</td>

    <td>&nbsp;

&nbsp;

</td>

    <td>&nbsp;

&nbsp;

</td>

  </tr>

<tr bgcolor="#FFFFFF">


              <td width="11%">第4节(11:10-12:00)</td>
             
  
    <td>&nbsp;

&nbsp;

</td>

    <td>&nbsp;

&nbsp;

</td>

    <td>&nbsp;

&nbsp;

</td>

    <td>&nbsp;

     基础英语3_01(校本部教三楼3-326)<br>

</td>

    <td>&nbsp;

     汉语阅读与写作_01(校本部教三楼3-417)<br>

</td>

    <td>&nbsp;

&nbsp;

</td>

    <td>&nbsp;

&nbsp;

</td>

<tr bgcolor="#FFFFFF">
    <td colspan="9">&nbsp;<p align="center" class="td2 style5"><strong>午 休</strong></p></td>
</tr>

  </tr>

<tr bgcolor="#FFFFFF">

<td width="3%" rowspan="4">&nbsp;<p class="style4">下午</p></td>


              <td width="11%">第5节(13:30-14:20)</td>
             
  
    <td>&nbsp;

     英语初级写作2_01(校本部教三楼3-326)<br>

</td>

    <td>&nbsp;

     基础英语3_01(校本部教三楼3-326)<br>

</td>

    <td>&nbsp;

&nbsp;

</td>

    <td>&nbsp;

     体育专项(上)_49(校本部体育场体育场)<br>

</td>

    <td>&nbsp;

     英语国家社会与文化_01(校本部教三楼3-546)<br>

</td>

    <td>&nbsp;

&nbsp;

</td>

    <td>&nbsp;

&nbsp;

</td>

  </tr>

<tr bgcolor="#FFFFFF">


              <td width="11%">第6节(14:30-15:20)</td>
             
  
    <td>&nbsp;

     英语初级写作2_01(校本部教三楼3-326)<br>

</td>

    <td>&nbsp;

     基础英语3_01(校本部教三楼3-326)<br>

</td>

    <td>&nbsp;

&nbsp;

</td>

    <td>&nbsp;

     体育专项(上)_49(校本部体育场体育场)<br>

</td>

    <td>&nbsp;

     英语国家社会与文化_01(校本部教三楼3-546)<br>

</td>

    <td>&nbsp;

&nbsp;

</td>

    <td>&nbsp;

&nbsp;

</td>

  </tr>

<tr bgcolor="#FFFFFF">


              <td width="11%">第7节(15:30-16:20)</td>
             
  
    <td>&nbsp;

&nbsp;

</td>

    <td>&nbsp;

     英语中级听力1_01(校本部教一楼1-301)<br>

</td>

    <td>&nbsp;

&nbsp;

</td>

    <td>&nbsp;

     形势与政策3_22(校本部教二楼2-441)<br>

</td>

    <td>&nbsp;

     时文选读_01(校本部教三楼3-546)<br>

</td>

    <td>&nbsp;

&nbsp;

</td>

    <td>&nbsp;

&nbsp;

</td>

  </tr>

<tr bgcolor="#FFFFFF">


              <td width="11%">第8节(16:30-17:20)</td>
             
  
    <td>&nbsp;

&nbsp;

</td>

    <td>&nbsp;

     英语中级听力1_01(校本部教一楼1-301)<br>

</td>

    <td>&nbsp;

&nbsp;

</td>

    <td>&nbsp;

     形势与政策3_22(校本部教二楼2-441)<br>

</td>

    <td>&nbsp;

     时文选读_01(校本部教三楼3-546)<br>

</td>

    <td>&nbsp;

&nbsp;

</td>

    <td>&nbsp;

&nbsp;

</td>

<tr bgcolor="#FFFFFF">
    <td colspan="9">&nbsp;<p align="center" class="td2 style5"><strong>晚 饭</strong></p></td>
</tr>

  </tr>

<tr bgcolor="#FFFFFF">

<td width="3%" rowspan="5">&nbsp;<p class="style4">晚上</p></td>


              <td width="11%">第9节(17:30-18:20)</td>
             
  
    <td>&nbsp;

&nbsp;

</td>

    <td>&nbsp;

&nbsp;

</td>

    <td>&nbsp;

&nbsp;

</td>

    <td>&nbsp;

&nbsp;

</td>

    <td>&nbsp;

&nbsp;

</td>

    <td>&nbsp;

&nbsp;

</td>

    <td>&nbsp;

&nbsp;

</td>

  </tr>

<tr bgcolor="#FFFFFF">


              <td width="11%">第10节(18:30-19:20)</td>
             
  
    <td>&nbsp;

&nbsp;

</td>

    <td>&nbsp;

&nbsp;

</td>

    <td>&nbsp;

     金属腐蚀和防护_02(校本部教三楼3-546)<br>

</td>

    <td>&nbsp;

&nbsp;

</td>

    <td>&nbsp;

&nbsp;

</td>

    <td>&nbsp;

&nbsp;

</td>

    <td>&nbsp;

&nbsp;

</td>

  </tr>

<tr bgcolor="#FFFFFF">


              <td width="11%">第11节(19:30-20:20)</td>
             
  
    <td>&nbsp;

&nbsp;

</td>

    <td>&nbsp;

&nbsp;

</td>

    <td>&nbsp;

     金属腐蚀和防护_02(校本部教三楼3-546)<br>

</td>

    <td>&nbsp;

&nbsp;

</td>

    <td>&nbsp;

&nbsp;

</td>

    <td>&nbsp;

&nbsp;

</td>

    <td>&nbsp;

&nbsp;

</td>

  </tr>

<tr bgcolor="#FFFFFF">


              <td width="11%">第12节(20:30-21:20)</td>
             
  
    <td>&nbsp;

&nbsp;

</td>

    <td>&nbsp;

&nbsp;

</td>

    <td>&nbsp;

&nbsp;

</td>

    <td>&nbsp;

&nbsp;

</td>

    <td>&nbsp;

&nbsp;

</td>

    <td>&nbsp;

&nbsp;

</td>

    <td>&nbsp;

&nbsp;

</td>

  </tr>

<tr bgcolor="#FFFFFF">


              <td width="11%">第13节(21:30-22:20)</td>
             
  
    <td>&nbsp;

&nbsp;

</td>

    <td>&nbsp;

&nbsp;

</td>

    <td>&nbsp;

&nbsp;

</td>

    <td>&nbsp;

&nbsp;

</td>

    <td>&nbsp;

&nbsp;

</td>

    <td>&nbsp;

&nbsp;

</td>

    <td>&nbsp;

&nbsp;

</td>

  </tr>

</table>
</td>
</tr>
</table>

<!--





<table width="100%" border="0" align="center" cellpadding="0" cellspacing="0">
<tr><td class="Linetop"></td>
</tr>
</table>
<table width="100%"  border="0" cellpadding="0" cellspacing="0" class="title" id="tblHead">
 <tr>
  <td>
   <table border="0" width="100%" cellpadding="0" cellspacing="0" >
   <tr>
   <td width="50%" align="left" valign="middle">&nbsp;<b>选课结果列表</b>&nbsp;</td>

<td width="50%" align="right">

</td>
</tr>
   </table>
  </tr>
</table>
<table width="100%" border="0" align="center" cellpadding="0" cellspacing="0"  >
 <tr>
  <td class="Linetop"></td>
 </tr>
</table>
-->







<link href="/css/newcss/project.css" rel="stylesheet" type="text/css">
 



<table width="100%" border="0" cellpadding="0" cellspacing="0" class="titleTop2">
                     <tr>
                      <td class="pageAlign">
                       <table cellpadding="0" width="100%" class="displayTag" cellspacing="1" border="0" id="user">
                        <thead>
                            <tr>






<th align="center" width="220" class="sortable">培养方案</th>




<th align="center" width="100" class="sortable">课程号</th>




<th align="center" width="100" class="sortable">课程名</th>




<th align="center" width="100" class="sortable">课序号</th>




<th align="center" width="100" class="sortable">学分</th>




<th align="center" width="100" class="sortable">课程属性</th>




<th align="center" width="100" class="sortable">考试类型</th>




<th align="center" width="100" class="sortable">教师</th>




<th align="center" width="100" class="sortable">大纲日历</th>




<th align="center" width="100" class="sortable">修读方式</th>




<th align="center" width="100" class="sortable">选课状态</th>




<th align="center" width="100" class="sortable">周次</th>




<th align="center" width="100" class="sortable">星期</th>




<th align="center" width="100" class="sortable">节次</th>




<th align="center" width="100" class="sortable">节数</th>




<th align="center" width="100" class="sortable">校区</th>




<th align="center" width="100" class="sortable">教学楼</th>




<th align="center" width="100" class="sortable">教室</th>


</tr>
</thead>



<tr class="odd" onMouseOut="this.className='even';" onMouseOver="this.className='evenfocus';">



        <td rowspan="2" >
    &nbsp;2011级 英语专业培养方案</td>


        <td rowspan="2" >
    &nbsp;3141040</td>


        <td rowspan="2" >
    &nbsp;基础英语3</td>


        <td rowspan="2" >
    &nbsp;01</td>


        <td rowspan="2" >
    &nbsp;4.0</td>


        <td rowspan="2" >
    &nbsp;必修</td>


        <td rowspan="2" >
    &nbsp;考试</td>


        <td rowspan="2" >
    &nbsp;郭艳玲* </td>


        <td rowspan="2" align="center">
    <img src="/img/icon/calendar.jpg" style="cursor: hand;" title="大纲日历" onclick="CxJxDgRl(this)" name="actionType=6&oper=QueryDgRl&kch=3141040&kxh=01"></td>


        <td rowspan="2" >
    &nbsp;正常</td>


        <td rowspan="2" >
    &nbsp;置入</td>




<td>&nbsp; 教学周：第 4-19 周</td>

<td>&nbsp; 4</td>

              <td>&nbsp;3</td>
             
<td>&nbsp; 2</td>

<td>&nbsp; 校本部</td>

<td>&nbsp; 教三楼</td>

<td>&nbsp; 3-326</td>

</tr>


<tr class=odd onMouseOut=this.className='even'; onMouseOver=this.className='evenfocus';>

<td>&nbsp; 教学周：第 4-19 周</td>

<td>&nbsp; 2</td>

              <td>&nbsp;5</td>
             
<td>&nbsp; 2</td>

<td>&nbsp; 校本部</td>

<td>&nbsp; 教三楼</td>

<td>&nbsp; 3-326</td>

</tr>


<tr class="odd" onMouseOut="this.className='even';" onMouseOver="this.className='evenfocus';">



        <td rowspan="1" >
    &nbsp;2011级 英语专业培养方案</td>


        <td rowspan="1" >
    &nbsp;3141080</td>


        <td rowspan="1" >
    &nbsp;英语泛读3</td>


        <td rowspan="1" >
    &nbsp;01</td>


        <td rowspan="1" >
    &nbsp;2.0</td>


        <td rowspan="1" >
    &nbsp;必修</td>


        <td rowspan="1" >
    &nbsp;考查</td>


        <td rowspan="1" >
    &nbsp;王斌* </td>


        <td rowspan="1" align="center">
    <img src="/img/icon/calendar.jpg" style="cursor: hand;" title="大纲日历" onclick="CxJxDgRl(this)" name="actionType=6&oper=QueryDgRl&kch=3141080&kxh=01"></td>


        <td rowspan="1" >
    &nbsp;正常</td>


        <td rowspan="1" >
    &nbsp;置入</td>




<td>&nbsp; 教学周：第 4-19 周</td>

<td>&nbsp; 2</td>

              <td>&nbsp;1</td>
             
<td>&nbsp; 2</td>

<td>&nbsp; 校本部</td>

<td>&nbsp; 教三楼</td>

<td>&nbsp; 3-426</td>

</tr>


<tr class="odd" onMouseOut="this.className='even';" onMouseOver="this.className='evenfocus';">



        <td rowspan="1" >
    &nbsp;2011级 英语专业培养方案</td>


        <td rowspan="1" >
    &nbsp;3141120</td>


        <td rowspan="1" >
    &nbsp;英语中级听力1</td>


        <td rowspan="1" >
    &nbsp;01</td>


        <td rowspan="1" >
    &nbsp;2.0</td>


        <td rowspan="1" >
    &nbsp;必修</td>


        <td rowspan="1" >
    &nbsp;考试</td>


        <td rowspan="1" >
    &nbsp;赵红* </td>


        <td rowspan="1" align="center">
    <img src="/img/icon/calendar.jpg" style="cursor: hand;" title="大纲日历" onclick="CxJxDgRl(this)" name="actionType=6&oper=QueryDgRl&kch=3141120&kxh=01"></td>


        <td rowspan="1" >
    &nbsp;正常</td>


        <td rowspan="1" >
    &nbsp;置入</td>




<td>&nbsp; 教学周：第 4-19 周</td>

<td>&nbsp; 2</td>

              <td>&nbsp;7</td>
             
<td>&nbsp; 2</td>

<td>&nbsp; 校本部</td>

<td>&nbsp; 教一楼</td>

<td>&nbsp; 1-301</td>

</tr>


<tr class="odd" onMouseOut="this.className='even';" onMouseOver="this.className='evenfocus';">



        <td rowspan="1" >
    &nbsp;2011级 英语专业培养方案</td>


        <td rowspan="1" >
    &nbsp;3141160</td>


        <td rowspan="1" >
    &nbsp;英语中级口语1</td>


        <td rowspan="1" >
    &nbsp;01</td>


        <td rowspan="1" >
    &nbsp;2.0</td>


        <td rowspan="1" >
    &nbsp;必修</td>


        <td rowspan="1" >
    &nbsp;考查</td>


        <td rowspan="1" >
    &nbsp;外教02* </td>


        <td rowspan="1" align="center">
    <img src="/img/icon/calendar.jpg" style="cursor: hand;" title="大纲日历" onclick="CxJxDgRl(this)" name="actionType=6&oper=QueryDgRl&kch=3141160&kxh=01"></td>


        <td rowspan="1" >
    &nbsp;正常</td>


        <td rowspan="1" >
    &nbsp;置入</td>




<td>&nbsp; 教学周：第 4-19 周</td>

<td>&nbsp; 1</td>

              <td>&nbsp;1</td>
             
<td>&nbsp; 2</td>

<td>&nbsp; 校本部</td>

<td>&nbsp; 教三楼</td>

<td>&nbsp; 3-428</td>

</tr>


<tr class="odd" onMouseOut="this.className='even';" onMouseOver="this.className='evenfocus';">



        <td rowspan="1" >
    &nbsp;2011级 英语专业培养方案</td>


        <td rowspan="1" >
    &nbsp;3141190</td>


        <td rowspan="1" >
    &nbsp;英语初级写作2</td>


        <td rowspan="1" >
    &nbsp;01</td>


        <td rowspan="1" >
    &nbsp;2.0</td>


        <td rowspan="1" >
    &nbsp;必修</td>


        <td rowspan="1" >
    &nbsp;考查</td>


        <td rowspan="1" >
    &nbsp;罗雨青* </td>


        <td rowspan="1" align="center">
    <img src="/img/icon/calendar.jpg" style="cursor: hand;" title="大纲日历" onclick="CxJxDgRl(this)" name="actionType=6&oper=QueryDgRl&kch=3141190&kxh=01"></td>


        <td rowspan="1" >
    &nbsp;正常</td>


        <td rowspan="1" >
    &nbsp;置入</td>




<td>&nbsp; 教学周：第 4-19 周</td>

<td>&nbsp; 1</td>

              <td>&nbsp;5</td>
             
<td>&nbsp; 2</td>

<td>&nbsp; 校本部</td>

<td>&nbsp; 教三楼</td>

<td>&nbsp; 3-326</td>

</tr>


<tr class="odd" onMouseOut="this.className='even';" onMouseOver="this.className='evenfocus';">



        <td rowspan="1" >
    &nbsp;2011级 英语专业培养方案</td>


        <td rowspan="1" >
    &nbsp;3141200</td>


        <td rowspan="1" >
    &nbsp;汉语阅读与写作</td>


        <td rowspan="1" >
    &nbsp;01</td>


        <td rowspan="1" >
    &nbsp;2.0</td>


        <td rowspan="1" >
    &nbsp;必修</td>


        <td rowspan="1" >
    &nbsp;考试</td>


        <td rowspan="1" >
    &nbsp;于奎战* </td>


        <td rowspan="1" align="center">
    <img src="/img/icon/calendar.jpg" style="cursor: hand;" title="大纲日历" onclick="CxJxDgRl(this)" name="actionType=6&oper=QueryDgRl&kch=3141200&kxh=01"></td>


        <td rowspan="1" >
    &nbsp;正常</td>


        <td rowspan="1" >
    &nbsp;置入</td>




<td>&nbsp; 教学周：第 4-19 周</td>

<td>&nbsp; 5</td>

              <td>&nbsp;3</td>
             
<td>&nbsp; 2</td>

<td>&nbsp; 校本部</td>

<td>&nbsp; 教三楼</td>

<td>&nbsp; 3-417</td>

</tr>


<tr class="odd" onMouseOut="this.className='even';" onMouseOver="this.className='evenfocus';">



        <td rowspan="1" >
    &nbsp;2011级 英语专业培养方案</td>


        <td rowspan="1" >
    &nbsp;8300003</td>


        <td rowspan="1" >
    &nbsp;形势与政策3</td>


        <td rowspan="1" >
    &nbsp;22</td>


        <td rowspan="1" >
    &nbsp;0.4</td>


        <td rowspan="1" >
    &nbsp;必修</td>


        <td rowspan="1" >
    &nbsp;考查</td>


        <td rowspan="1" >
    &nbsp;宣传部02* </td>


        <td rowspan="1" align="center">
    <img src="/img/icon/calendar.jpg" style="cursor: hand;" title="大纲日历" onclick="CxJxDgRl(this)" name="actionType=6&oper=QueryDgRl&kch=8300003&kxh=22"></td>


        <td rowspan="1" >
    &nbsp;正常</td>


        <td rowspan="1" >
    &nbsp;置入</td>




<td>&nbsp; 10-12周上</td>

<td>&nbsp; 4</td>

              <td>&nbsp;7</td>
             
<td>&nbsp; 2</td>

<td>&nbsp; 校本部</td>

<td>&nbsp; 教二楼</td>

<td>&nbsp; 2-441</td>

</tr>


<tr class="odd" onMouseOut="this.className='even';" onMouseOver="this.className='evenfocus';">



        <td rowspan="1" >
    &nbsp;2011级 英语专业培养方案</td>


        <td rowspan="1" >
    &nbsp;3330012</td>


        <td rowspan="1" >
    &nbsp;体育专项(上)</td>


        <td rowspan="1" >
    &nbsp;49</td>


        <td rowspan="1" >
    &nbsp;2.0</td>


        <td rowspan="1" >
    &nbsp;必修</td>


        <td rowspan="1" >
    &nbsp;考查</td>


        <td rowspan="1" >
    &nbsp;刘泳* </td>


        <td rowspan="1" align="center">
    <img src="/img/icon/calendar.jpg" style="cursor: hand;" title="大纲日历" onclick="CxJxDgRl(this)" name="actionType=6&oper=QueryDgRl&kch=3330012&kxh=49"></td>


        <td rowspan="1" >
    &nbsp;正常</td>


        <td rowspan="1" >
    &nbsp;选中</td>




<td>&nbsp; 教学周：第 4-19 周</td>

<td>&nbsp; 4</td>

              <td>&nbsp;5</td>
             
<td>&nbsp; 2</td>

<td>&nbsp; 校本部</td>

<td>&nbsp; 体育场</td>

<td>&nbsp; 体育场</td>

</tr>


<tr class="odd" onMouseOut="this.className='even';" onMouseOver="this.className='evenfocus';">



        <td rowspan="1" >
    &nbsp;2011级 英语专业培养方案</td>


        <td rowspan="1" >
    &nbsp;3141260</td>


        <td rowspan="1" >
    &nbsp;英语国家社会与文化</td>


        <td rowspan="1" >
    &nbsp;01</td>


        <td rowspan="1" >
    &nbsp;2.0</td>


        <td rowspan="1" >
    &nbsp;选修</td>


        <td rowspan="1" >
    &nbsp;考查</td>


        <td rowspan="1" >
    &nbsp;外教03* </td>


        <td rowspan="1" align="center">
    <img src="/img/icon/calendar.jpg" style="cursor: hand;" title="大纲日历" onclick="CxJxDgRl(this)" name="actionType=6&oper=QueryDgRl&kch=3141260&kxh=01"></td>


        <td rowspan="1" >
    &nbsp;正常</td>


        <td rowspan="1" >
    &nbsp;选中</td>




<td>&nbsp; 教学周：第 4-19 周</td>

<td>&nbsp; 5</td>

              <td>&nbsp;5</td>
             
<td>&nbsp; 2</td>

<td>&nbsp; 校本部</td>

<td>&nbsp; 教三楼</td>

<td>&nbsp; 3-546</td>

</tr>


<tr class="odd" onMouseOut="this.className='even';" onMouseOver="this.className='evenfocus';">



        <td rowspan="1" >
    &nbsp;2011级 英语专业培养方案</td>


        <td rowspan="1" >
    &nbsp;3141320</td>


        <td rowspan="1" >
    &nbsp;时文选读</td>


        <td rowspan="1" >
    &nbsp;01</td>


        <td rowspan="1" >
    &nbsp;2.0</td>


        <td rowspan="1" >
    &nbsp;选修</td>


        <td rowspan="1" >
    &nbsp;考查</td>


        <td rowspan="1" >
    &nbsp;外教03* </td>


        <td rowspan="1" align="center">
    <img src="/img/icon/calendar.jpg" style="cursor: hand;" title="大纲日历" onclick="CxJxDgRl(this)" name="actionType=6&oper=QueryDgRl&kch=3141320&kxh=01"></td>


        <td rowspan="1" >
    &nbsp;正常</td>


        <td rowspan="1" >
    &nbsp;选中</td>




<td>&nbsp; 教学周：第 4-19 周</td>

<td>&nbsp; 5</td>

              <td>&nbsp;7</td>
             
<td>&nbsp; 2</td>

<td>&nbsp; 校本部</td>

<td>&nbsp; 教三楼</td>

<td>&nbsp; 3-546</td>

</tr>


<tr class="odd" onMouseOut="this.className='even';" onMouseOver="this.className='evenfocus';">



        <td rowspan="1" >
    &nbsp;2011级 英语专业培养方案</td>


        <td rowspan="1" >
    &nbsp;4143020</td>


        <td rowspan="1" >
    &nbsp;金属腐蚀和防护</td>


        <td rowspan="1" >
    &nbsp;02</td>


        <td rowspan="1" >
    &nbsp;2.0</td>


        <td rowspan="1" >
    &nbsp;任选</td>


        <td rowspan="1" >
    &nbsp;考查</td>


        <td rowspan="1" >
    &nbsp;张瑾* </td>


        <td rowspan="1" align="center">
    <img src="/img/icon/calendar.jpg" style="cursor: hand;" title="大纲日历" onclick="CxJxDgRl(this)" name="actionType=6&oper=QueryDgRl&kch=4143020&kxh=02"></td>


        <td rowspan="1" >
    &nbsp;正常</td>


        <td rowspan="1" >
    &nbsp;选中</td>




<td>&nbsp; 教学周：第 4-19 周</td>

<td>&nbsp; 3</td>

              <td>&nbsp;10</td>
             
<td>&nbsp; 2</td>

<td>&nbsp; 校本部</td>

<td>&nbsp; 教三楼</td>

<td>&nbsp; 3-546</td>

</tr>

</table>
</td>
</tr>
</table>
<Script language="JavaScript">
function CxJxDgRl( a){
    window.open("xkAction.do?"+a.name);
}
</Script>











<table width="100%" align="center" cellpadding="0" cellspacing="0">
<tr>

<td height="21" bgcolor="#F2F2F2"><div align="right">共22.4学分</div></td>

</tr>
</table>  










</body>
</html>
"""
    soup = BeautifulSoup(doc)
