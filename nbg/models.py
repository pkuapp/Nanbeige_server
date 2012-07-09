from django.db import models
from django.conf import settings

class App(models.Model):
    version_android = models.CharField(max_length=30)
    version_ios = models.CharField(max_length=30)

class University(models.Model):
    name = models.CharField(max_length=200)

class Course(models.Model):
    name = models.CharField(max_length=200)
    
class Building(models.Model):
    name = models.CharField(max_length=30)
    university = models.ForeignKey(University)
    latitude = models.DecimalField(max_digits=10, decimal_places=6)
    longitude = models.DecimalField(max_digits=10, decimal_places=6)

class Classroom(models.Model):
    name = models.CharField(max_length=30)
    building = models.ForeignKey(Building)

class ClassroomAvailability(models.Model):
    classroom = models.ForeignKey(Classroom)
    date = models.DateField()
    isAvailable = models.BooleanField()

