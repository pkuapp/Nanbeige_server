from django.db import models
from django.conf import settings

class App(models.Model):
    version_android_beta = models.CharField(max_length=30)
    version_android_stable = models.CharField(max_length=30)
    version_ios_beta = models.CharField(max_length=30)
    version_ios_stable = models.CharField(max_length=30)
    notice = models.TextField()

class University(models.Model):
    name = models.CharField(max_length=200)
    english_name = models.CharField(max_length=200)
    latitude = models.DecimalField(max_digits=10, decimal_places=6)
    longitude = models.DecimalField(max_digits=10, decimal_places=6)

class Course(models.Model):
    name = models.CharField(max_length=200)
    original_id = models.CharField(max_length=100)
    credit = models.DecimalField(max_digits=3, decimal_places=1)
    weeks = models.CommaSeparatedIntegerField(max_length=100)

class Lesson(models.Model):
    day = models.SmallIntegerField()
    start = models.SmallIntegerField()
    end = models.SmallIntegerField()
    location = models.CharField(max_length=200)
    course = models.ForeignKey(Course)

class Teacher(models.Model):
    name = models.CharField(max_length=50)
    course = models.ForeignKey(Course)

class Ta(models.Model):
    name = models.CharField(max_length=50)

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
    availability = models.BooleanField()
