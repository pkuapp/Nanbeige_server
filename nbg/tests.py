"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from django.test.client import Client
import json

class SimpleTest(TestCase):
    def test_basic_addition(self):
        """
        Tests that 1 + 1 always equals 2.
        """
        self.assertEqual(1 + 1, 2)

class AvalaibleTest(TestCase):
    c = Client()
    def test_univercity_list(self):
        response = self.c.get('/university/')
        assert(response.status_code,200)
        assert(isinstance(json.loads(response.read(),list),True))