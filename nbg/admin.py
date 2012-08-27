from django.contrib import admin
from nbg.models import *

class CourseAdmin(admin.ModelAdmin):
    def lessons(self, course):
        ret = ""
        for l in course.lesson_set.values():
            l['location'] = l['location'].encode('utf8')
            l['weeks'] = l['weeks'].encode('utf8')

            ret += "{day} {start}-{end}, [{weeks}], {location}; ".format(**l)
        return ret

    search_fields = ['name']
    list_display = ('id', 'semester', 'original_id', 'name', 'teacher', 'lessons')

class UserProfileAdmin(admin.ModelAdmin):
    raw_id_fields = ('courses',)

class UserActionAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'semester', 'action_type')

admin.site.register(App)
admin.site.register(University)
admin.site.register(Campus)
admin.site.register(Semester)
admin.site.register(ScheduleUnit)
admin.site.register(Course, CourseAdmin)
admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(UserAction, UserActionAdmin)
admin.site.register(Lesson)
admin.site.register(Assignment)
admin.site.register(Comment)
admin.site.register(Building)
admin.site.register(Room)
admin.site.register(RoomAvailability)
admin.site.register(EventCategory)
admin.site.register(Event)
admin.site.register(WikiNode)
admin.site.register(Wiki)
