# -*- coding: utf-8 -*-

"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from django.test.client import Client
from django_nose import FastFixtureTestCase
import json

class AvalaibleTest(TestCase):

    fixtures = ['dump.yaml',]

    def setUp(self):
        self.c = Client()

    def test_app_meta(self):
        urls = []
        urls.extend(['/app/' + u for u in (
            'version/api/',
            'version/android/',
            'version/ios/',
            'notice/'
            )])
        for url in urls:
            response = self.c.get(url)
            assert response.status_code == 200

    def test_university(self):

        urls = []
        urls.extend(['/university/' + u for u in (
            '',
            '1/',
            '1/semester/'
            )])
        for url in urls:
            response = self.c.get(url)
            assert response.status_code == 200

    def test_study(self):
        urls = []
        # urls.extend(['/study/' + u for u in (
        #     'building/',
        #     'building/'
        #     )])
    
    def test_wiki(self):
        urls = ['/wiki/1/','/wiki/node/1/']
        for url in urls:
            response = self.c.get(url)
            assert response.status_code == 200

    def test_login(self):
        response = self.c.post('/user/login/email/',\
            {'email':'coolgene@gmail.com','password':'coolgene'})
        assert isinstance(json.loads(response.content)['id'],int)



class LogicTest(TestCase):

    fixtures = ['dump.yaml',]

    def setUp(self):
        self.c = Client()
        self.c.login(username='coolgene@gmail.com', password='coolgene')

    def test_univercity_list(self):
        response = self.c.get('/university/')
        assert isinstance(json.loads(response.content),list)

    def test_courses(self):
        response = self.c.get('/course/')
        assert isinstance(json.loads(response.content),list)

    def test_assignment(self):
        urlr = ('/course/assignment/')

        response = self.c.post(urlr+'add/',\
            {
                'course_id':1, 
                'due':"2013-01-14 00:00:00",
                'content':'请吴昊天吃饭',
            })

        assert response.status_code == 200
        assert type(json.loads(response.content)['id']) is int
        assignment_id = json.loads(response.content)['id']

        response = self.c.get(urlr)
        assert response.status_code == 200
        assert isinstance(json.loads(response.content),list)
        assert not json.loads(response.content)[-1]['finished']


        response = self.c.post(urlr+'%s/finish/' % (assignment_id),{'finished':1})
        assert response.status_code == 200
        response = self.c.get(urlr)
        assert json.loads(response.content)[-1]['finished']

        response = self.c.post(urlr+'%s/finish/' % (assignment_id),{'finished':0})
        assert response.status_code == 200
        response = self.c.get(urlr)
        assert not json.loads(response.content)[-1]['finished']


        resposne = self.c.post(urlr+'%s/modify/' % (assignment_id),\
            {
                'course_id':1, 
                'due':"2014-01-14 00:00:00",
                'content':'请吴昊天吃金钱豹', 
            })
        assert response.status_code == 200
        response = self.c.post(urlr)
        assert json.loads(response.content)[-1]['content'] is '请吴昊天吃金钱豹'

        response = self.c.post('/course/%s/delete/' % (assignment_id))
        assert response.status_code == 200
        response = self.c.get(urlr)
        assert json.loads(response.content)[-1]['id'] is not int(assignment_id)
