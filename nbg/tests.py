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
            assert response.status_code, 200

    def test_university(self):
        urls = []
        urls.extend(['/university/' + u for u in (
            '',
            '1/',
            '1/semester/'
            )])
        for url in urls:
            response = self.c.get(url)
            assert response.status_code, 200

class UniversityAvalaibleTest(TestCase):
    fixtures = ['dump.yaml',]
    def setUp(self):
        self.c = Client()



class AdvancedTest(TestCase):
    def setUp(self):
        self.c = Client()

    def test_univercity_list(self):
        response = self.c.get('/university/')
        assert isinstance(json.loads(response.content),list), True