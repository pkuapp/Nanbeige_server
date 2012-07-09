from django.db import models
from django.conf import settings

class App(models.Model):
    version_android = models.CharField(max_length=30)
    version_ios = models.CharField(max_length=30)
