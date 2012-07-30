#! python
# -*- coding: utf-8 -*-

from types import *
from BeautifulSoup import *
import urllib,urllib2
import re
from django.contrib.models import User
from nbg.models import *

def account_handler(username, password):
        