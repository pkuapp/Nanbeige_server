from django.db import models
from datetime import datetime
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin

class App(models.Model):
    version_android_beta = models.CharField(max_length=30)
    version_android_stable = models.CharField(max_length=30)
    version_ios_beta = models.CharField(max_length=30)
    version_ios_stable = models.CharField(max_length=30)
    notice_time = models.DateTimeField()
    notice_content = models.TextField()

class University(models.Model):
    name = models.CharField(max_length=200)
    english_name = models.CharField(max_length=200)
    latitude = models.DecimalField(max_digits=10, decimal_places=6)
    longitude = models.DecimalField(max_digits=10, decimal_places=6)
    support_import_course = models.BooleanField()
    support_list_course = models.BooleanField()
    week_start = models.DateField()
    week_end = models.DateField()
    excluded = models.CommaSeparatedIntegerField(max_length=100)
    lessons_morning = models.SmallIntegerField()
    lessons_afternoon = models.SmallIntegerField()
    lessons_evening = models.SmallIntegerField()

class UserProfile(models.Model):
    user = models.OneToOneField(User)
    weibo_token = models.CharField(max_length=32)

class ScheduleUnit(models.Model):
    number = models.SmallIntegerField()
    start = models.TimeField()
    end = models.TimeField()
    university = models.ForeignKey(University)

class Course(models.Model):
    name = models.CharField(max_length=200)
    original_id = models.CharField(max_length=100)
    credit = models.DecimalField(max_digits=3, decimal_places=1)
    weeks = models.CommaSeparatedIntegerField(max_length=200)

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
    course = models.ForeignKey(Course)

class Assignment(models.Model):
    course = models.ForeignKey(Course)
    user = models.ForeignKey(User)
    due = models.DateTimeField()
    content = models.TextField()
    finished = models.BooleanField()
    last_modified = models.DateTimeField()

class Comment(models.Model):
    course = models.ForeignKey(Course)
    writer = models.ForeignKey(User)
    time = models.DateTimeField()
    content = models.TextField()

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

class EventCategory(models.Model):
    name = models.CharField(max_length=200)

    def count(self):
        return self.event_set.filter(time__gte=datetime.now()).count()

class Event(models.Model):
    title = models.CharField(max_length=200)
    subtitle = models.CharField(max_length=200)
    category = models.ForeignKey(EventCategory)
    time = models.DateTimeField()
    location = models.CharField(max_length=200)
    organizer = models.CharField(max_length=200)
    content = models.TextField()
    follower = models.ManyToManyField(User)

    def follow_count(self):
        return self.follower.count()

class WikiNode(models.Model):
    TYPE_CHOICES = (
        ('A', 'Article'),
        ('L', 'List'),
    )
    title = models.CharField(max_length=200)
    father = models.ForeignKey('self', null=True)
    type = models.CharField(max_length=1, choices=TYPE_CHOICES)
    content = models.TextField()

class Wiki(models.Model):
    university = models.ForeignKey(University)
    node = models.ForeignKey(WikiNode)
