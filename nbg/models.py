# -*- coding: utf-8 -*-

from django.db import models
from datetime import datetime
from django.contrib.auth.models import User
from django.db.models.signals import class_prepared
from django.contrib.auth.models import UserManager as Manager
from couchdb.client import Server, Database
from couchdb.http import PreconditionFailed
from django.db.models.signals import post_save

COUCHDB_HOST = 'http://211.101.12.224'
COUCHDB_PORT = '5984'
server = Server('{0}:{1}'.format(COUCHDB_HOST, COUCHDB_PORT))
server.resource.credentials = ('nbgd4P4eCTr4Vb4xQmL', 'CFh1oF1yqILzCXlagD6K')
userdb = Database('{0}:{1}/_users'.format(COUCHDB_HOST, COUCHDB_PORT))
userdb.resource.credentials = ('nbgd4P4eCTr4Vb4xQmL', 'CFh1oF1yqILzCXlagD6K')

class UserManager(Manager):
    """automatically create corresponding user syncable database in couchdb"""
    def create_user(self, username, email=None, password=None):
        user = super(UserManager, self).create_user(username, email, password)
        if user:
            try:
                server.create('user_sync_db_{0}'.format(user.pk))
            except PreconditionFailed:
                user.delete()
                raise PreconditionFailed
        return user

def extend_username(sender, *args, **kwargs):
    """extend username max_length to 75"""
    if sender.__name__ == "User" and sender.__module__ == "django.contrib.auth.models":
        sender._meta.get_field("username").max_length = 75

class_prepared.connect(extend_username)

class UserProxy(User):
    objects = UserManager()

    class Meta:
        proxy = True

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
    support_ta = models.BooleanField()
    lessons_morning = models.SmallIntegerField()
    lessons_afternoon = models.SmallIntegerField()
    lessons_evening = models.SmallIntegerField()
    lessons_separator = models.CommaSeparatedIntegerField(max_length=50)

    def __unicode__(self):
        return u'#%s %s' % (self.id, self.name)

class ScheduleUnit(models.Model):
    number = models.SmallIntegerField()
    start = models.TimeField()
    end = models.TimeField()
    university = models.ForeignKey(University)

    def __unicode__(self):
        return u'#%s %s - 第%s节' % (self.id, self.university.name, self.number)

class Campus(models.Model):
    name = models.CharField(max_length=100, blank=True)
    university = models.ForeignKey(University)
    latitude = models.DecimalField(max_digits=10, decimal_places=6)
    longitude = models.DecimalField(max_digits=10, decimal_places=6)

    def __unicode__(self):
        return u'#%s %s%s' % (self.id, self.university.name, self.name)

class Semester(models.Model):
    name = models.CharField(max_length=100)
    year = models.CharField(max_length=50)
    university = models.ForeignKey(University)
    week_start = models.DateField()
    week_end = models.DateField()

    def __unicode__(self):
        return u'#%s %s - %s' % (self.id, self.university.name, self.name)

class Weekset(models.Model):
    name = models.CharField(max_length=100, blank=True)
    weeks = models.CommaSeparatedIntegerField(max_length=200, blank=True)
    semester = models.ForeignKey(Semester)

    def __unicode__(self):
        return self.name

class NewsFeed(models.Model):
    SELECT_COURSE = 0
    AUDIT_COURSE = 1
    COMMENT_COURSE = 2
    FOLLOW_COURSE = 3
    COMMENT_COURSE = 4
    NEWS_TYPE_CHOICES = ((SELECT_COURSE, 'select_course'), (AUDIT_COURSE, 'audit_course'))

    news_type = models.IntegerField(choices=NEWS_TYPE_CHOICES, null=False)
    ref_model = models.CharField(max_length=55, null=False)
    object_id = models.IntegerField(null=False)
    time = models.DateTimeField(auto_now_add=True)
    info = models.CharField(max_length=755, null=True)


class Course(models.Model):
    name = models.CharField(max_length=200)
    original_id = models.CharField(max_length=100)
    credit = models.DecimalField(max_digits=3, decimal_places=1, null=True)
    semester = models.ForeignKey(Semester)
    teacher = models.CharField(max_length=200, blank=True)
    ta = models.CharField(max_length=200, blank=True)
    custom = models.CharField(max_length=300, blank=True)

    def __unicode__(self):
        return u'#%s %s - %s' % (self.id, self.semester.university.name, self.name)

class UserProfile(models.Model):
    user = models.OneToOneField(User)
    weibo_id = models.BigIntegerField(null=True, blank=True)
    weibo_name = models.CharField(max_length=100, blank=True)
    weibo_token = models.CharField(max_length=32, blank=True)
    renren_id = models.BigIntegerField(null=True, blank=True)
    renren_name = models.CharField(max_length=100, blank=True)
    nickname = models.CharField(max_length=100, blank=True)
    realname = models.CharField(max_length=100, blank=True)
    courses = models.ManyToManyField(Course, blank=True, through='CourseStatus')
    campus = models.ForeignKey(Campus, null=True)

    def __unicode__(self):
        return u'#%s (#%s %s)' % (self.id, self.user.id, self.user.username)

class CourseStatus(models.Model):
    SELECT = 0
    AUDIT = 1
    STATUS_CHOICES = ((SELECT, 'select'), (AUDIT, 'audit'))
    user_profile = models.ForeignKey(UserProfile)
    course = models.ForeignKey(Course)
    status = models.IntegerField(choices=STATUS_CHOICES)


def generate_news_for_course_status(sender, **kwargs):
    instance = kwargs['instance']
    if instance.status == CourseStatus.SELECT:
        newsfeed_dict = {
            'news_type': NewsFeed.SELECT_COURSE,
            'ref_model': 'Course',
            'object_id': sender.course,
            'info': '{sender:{0}}'.format(sender.user_profile.nickname)
        }
        NewsFeed.objects.create(**newsfeed_dict)
    elif instance.status == CourseStatus.AUDIT:
        newsfeed_dict = {
            'news_type': NewsFeed.AUDIT_COURSE,
            'ref_model': 'Course',
            'object_id': sender.course,
            'info': '{sender:{0}}'.format(sender.user_profile.nickname)
        }
        NewsFeed.objects.create(**newsfeed_dict)

post_save.connect(generate_news_for_course_status, sender=CourseStatus)

class UserAction(models.Model):
    COURSE_IMPORTED = 0
    ACTION_CHOICES = ((COURSE_IMPORTED, 'Course Imported'),)
    user = models.ForeignKey(User)
    semester = models.ForeignKey(Semester)
    time = models.DateTimeField(auto_now_add=True)
    action_type = models.IntegerField(choices=ACTION_CHOICES)

class Lesson(models.Model):
    day = models.SmallIntegerField()
    start = models.SmallIntegerField()
    end = models.SmallIntegerField()
    weekset = models.ForeignKey(Weekset, null=True)
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
        return u'#%s %s - %s - %s' % (self.id, self.building.campus.university.name, self.building.name, self.name)

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

    def follower_count(self):
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
