# -*- coding: utf-8 -*-

from django.db import models
from datetime import datetime
from django.contrib.auth.models import User  

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
    support_import_course = models.BooleanField()
    support_list_course = models.BooleanField()
    lessons_morning = models.SmallIntegerField()
    lessons_afternoon = models.SmallIntegerField()
    lessons_evening = models.SmallIntegerField()
    lessons_separator = models.CommaSeparatedIntegerField(max_length=50)

    def __unicode__(self):
        return u'#%s %s' % (self.id, self.name)

class Campus(models.Model):
    name = models.CharField(max_length=100, blank=True)
    university = models.ForeignKey(University)
    latitude = models.DecimalField(max_digits=10, decimal_places=6)
    longitude = models.DecimalField(max_digits=10, decimal_places=6)

    def __unicode__(self):
        return u'#%s %s%s' % (self.id, self.university.name, self.name)

class Semester(models.Model):
    """
        excluded: 不同学校的公共假期或考试周等无课时间
    """
    name = models.CharField(max_length=100)
    year = models.CharField(max_length=50)
    university = models.ForeignKey(University)
    week_start = models.DateField()
    week_end = models.DateField()
    excluded = models.CommaSeparatedIntegerField(max_length=100, blank=True)

    def __unicode__(self):
        return  u'#%s %s - %s' % (self.id, self.university.name, self.name)

class ScheduleUnit(models.Model):
    number = models.SmallIntegerField()
    start = models.TimeField()
    end = models.TimeField()
    university = models.ForeignKey(University)

    def __unicode__(self):
        return u'#%s %s - 第%s节' % (self.id, self.university.name, self.number)

class Course(models.Model):
    name = models.CharField(max_length=200)
    original_id = models.CharField(max_length=100)
    credit = models.DecimalField(max_digits=3, decimal_places=1)
    semester = models.ForeignKey(Semester)
    teacher = models.CharField(max_length=200, blank=True)
    ta = models.CharField(max_length=200, blank=True)
    custom = models.CharField(max_length=300, blank=True)
    hash = models.CharField(max_length=32)

    def __unicode__(self):
        return u'#%s %s - %s' % (self.id, self.semester.university.name, self.name)

class UserProfile(models.Model):
    user = models.OneToOneField(User)
    weibo_name = models.CharField(max_length=120, blank=True)
    nickname = models.CharField(max_length=100, blank=True)
    courses = models.ManyToManyField(Course, blank=True)
    university = models.ForeignKey(University, null=True)

    def __unicode__(self):
        return u'#%s (#%s %s)' % (self.id, self.user.id, self.user.username)

class UserAction(models.Model):

    ACTION_CHOICES = ((0, 'courses_imported'),)

    user = models.ForeignKey(User)
    semester = models.ForeignKey(Semester)
    time = models.DateTimeField(auto_now_add=True)
    action_type = models.IntegerField(choices=ACTION_CHOICES)

class Lesson(models.Model):
    day = models.SmallIntegerField()
    start = models.SmallIntegerField()
    end = models.SmallIntegerField()
    weeks = models.CommaSeparatedIntegerField(max_length=200)
    location = models.CharField(max_length=200)
    course = models.ForeignKey(Course)

    def __unicode__(self):
        return u'#%s %s' % (self.id, self.course.name)

class Assignment(models.Model):
    course = models.ForeignKey(Course)
    user = models.ForeignKey(User)
    due = models.DateTimeField()
    content = models.TextField()
    finished = models.BooleanField(default=False)
    deleted = models.BooleanField(default=False)
    last_modified = models.DateTimeField()

    def __unicode__(self):
        return u'#%s %s - %s' % (self.id, self.user.username, self.course.name)

class Comment(models.Model):
    course = models.ForeignKey(Course)
    writer = models.ForeignKey(User)
    time = models.DateTimeField()
    content = models.TextField()

    def __unicode__(self):
        return u'#%s %s' % (self.id, self.course.name)

class Building(models.Model):
    name = models.CharField(max_length=30)
    campus = models.ForeignKey(Campus)
    latitude = models.DecimalField(max_digits=10, decimal_places=6)
    longitude = models.DecimalField(max_digits=10, decimal_places=6)

    def __unicode__(self):
        return u'#%s %s -  %s' % (self.id, self.campus, self.name)

class Room(models.Model):
    name = models.CharField(max_length=30)
    building = models.ForeignKey(Building)

    def __unicode__(self):
        return u'#%s %s - %s - %s' % (self.id, self.building.university.name, self.building.name, self.name)

class RoomAvailability(models.Model):
    room = models.ForeignKey(Room)
    date = models.DateField()
    availability = models.CommaSeparatedIntegerField(max_length=50)

    def __unicode__(self):
        return u'#%s %s' % (self.id, self.room.name)

class EventCategory(models.Model):
    name = models.CharField(max_length=200)

    def count(self):
        return self.event_set.filter(time__gte=datetime.now()).count()

    def __unicode__(self):
        return u'#%s %s' % (self.id, self.name)

class Event(models.Model):
    title = models.CharField(max_length=200)
    subtitle = models.CharField(max_length=200)
    category = models.ForeignKey(EventCategory)
    time = models.DateTimeField()
    campus = models.ForeignKey(Campus)
    location = models.CharField(max_length=200)
    organizer = models.CharField(max_length=200)
    content = models.TextField()
    follower = models.ManyToManyField(User, blank=True)

    def follow_count(self):
        return self.follower.count()

    def __unicode__(self):
        return u'#%s %s - %s' % (self.id, self.campus, self.title)

class WikiNode(models.Model):
    TYPE_CHOICES = (
        ('A', 'Article'),
        ('L', 'List'),
    )
    title = models.CharField(max_length=200)
    father = models.ForeignKey('self', null=True)
    type = models.CharField(max_length=1, choices=TYPE_CHOICES)
    content = models.TextField()

    def __unicode__(self):
        return u'#%s %s' % (self.id, self.title)

class Wiki(models.Model):
    university = models.ForeignKey(University)
    node = models.ForeignKey(WikiNode)

    def __unicode__(self):
        return u'#%s %s - %s' % (self.id, self.university.name, self.node.title)
