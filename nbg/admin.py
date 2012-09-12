# -*- coding: utf-8 -*-

from django.contrib import admin
from nbg.models import *

class WeeksetAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'semester', 'weeks')

class CourseAdmin(admin.ModelAdmin):
    def lessons(self, course):
        ret = ""
        for l in course.lesson_set.all():
            ret += "周{day} {start}-{end} {weekset} {location}; ".format(
              day=l.day, start=l.start, end=l.end, weekset=l.weekset, location=l.location.encode('utf8'))
        return ret

    search_fields = ('name', 'original_id')
    list_display = ('id', 'semester', 'original_id', 'name', 'credit', 'teacher', 'lessons')

class CourseStatusInline(admin.TabularInline):
    model = CourseStatus
    raw_id_fields = ('course',)

def user_id(user_profile):
    return user_profile.user.id

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('id', user_id, 'user', 'nickname', 'weibo_name', 'renren_name', 'campus')
    list_display_links = ('id', user_id)

    inlines = (CourseStatusInline,)

class CourseStatusAdmin(admin.ModelAdmin):
    list_display = ('user_profile', 'course', 'time', 'status')

class UserActionAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'semester', 'action_type')

admin.site.register(App)
admin.site.register(University)
admin.site.register(ScheduleUnit)
admin.site.register(Campus)
admin.site.register(Semester)
admin.site.register(Weekset, WeeksetAdmin)
admin.site.register(Course, CourseAdmin)
admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(CourseStatus, CourseStatusAdmin)
admin.site.register(UserAction, UserActionAdmin)
admin.site.register(Lesson)
admin.site.register(Comment)
admin.site.register(Building)
admin.site.register(Room)
admin.site.register(RoomAvailability)
admin.site.register(EventCategory)
admin.site.register(Event)
admin.site.register(WikiNode)
admin.site.register(Wiki)
