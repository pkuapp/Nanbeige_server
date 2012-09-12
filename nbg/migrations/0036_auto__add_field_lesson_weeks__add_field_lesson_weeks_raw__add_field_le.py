# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Lesson.weeks'
        db.add_column('nbg_lesson', 'weeks',
                      self.gf('django.db.models.fields.CommaSeparatedIntegerField')(default='', max_length=200, blank=True),
                      keep_default=False)

        # Adding field 'Lesson.weeks_raw'
        db.add_column('nbg_lesson', 'weeks_raw',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=200, blank=True),
                      keep_default=False)

        # Adding field 'Lesson.weeks_display'
        db.add_column('nbg_lesson', 'weeks_display',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=100, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Lesson.weeks'
        db.delete_column('nbg_lesson', 'weeks')

        # Deleting field 'Lesson.weeks_raw'
        db.delete_column('nbg_lesson', 'weeks_raw')

        # Deleting field 'Lesson.weeks_display'
        db.delete_column('nbg_lesson', 'weeks_display')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'nbg.app': {
            'Meta': {'object_name': 'App'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'notice_content': ('django.db.models.fields.TextField', [], {}),
            'notice_time': ('django.db.models.fields.DateTimeField', [], {}),
            'version_android_beta': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'version_android_stable': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'version_ios_beta': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'version_ios_stable': ('django.db.models.fields.CharField', [], {'max_length': '30'})
        },
        'nbg.assignment': {
            'Meta': {'object_name': 'Assignment'},
            'content': ('django.db.models.fields.TextField', [], {}),
            'course': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['nbg.Course']"}),
            'deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'due': ('django.db.models.fields.DateTimeField', [], {}),
            'finished': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_modified': ('django.db.models.fields.DateTimeField', [], {}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'nbg.building': {
            'Meta': {'object_name': 'Building'},
            'campus': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['nbg.Campus']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'latitude': ('django.db.models.fields.DecimalField', [], {'max_digits': '10', 'decimal_places': '6'}),
            'longitude': ('django.db.models.fields.DecimalField', [], {'max_digits': '10', 'decimal_places': '6'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30'})
        },
        'nbg.campus': {
            'Meta': {'object_name': 'Campus'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'latitude': ('django.db.models.fields.DecimalField', [], {'max_digits': '10', 'decimal_places': '6'}),
            'longitude': ('django.db.models.fields.DecimalField', [], {'max_digits': '10', 'decimal_places': '6'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'university': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['nbg.University']"})
        },
        'nbg.comment': {
            'Meta': {'object_name': 'Comment'},
            'content': ('django.db.models.fields.TextField', [], {}),
            'course': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['nbg.Course']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'time': ('django.db.models.fields.DateTimeField', [], {}),
            'writer': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'nbg.course': {
            'Meta': {'object_name': 'Course'},
            'credit': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '3', 'decimal_places': '1'}),
            'custom': ('django.db.models.fields.CharField', [], {'max_length': '300', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'original_id': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'semester': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['nbg.Semester']"}),
            'ta': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'teacher': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'})
        },
        'nbg.coursestatus': {
            'Meta': {'object_name': 'CourseStatus'},
            'course': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['nbg.Course']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'status': ('django.db.models.fields.IntegerField', [], {}),
            'time': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'user_profile': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['nbg.UserProfile']"})
        },
        'nbg.event': {
            'Meta': {'object_name': 'Event'},
            'campus': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['nbg.Campus']"}),
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['nbg.EventCategory']"}),
            'content': ('django.db.models.fields.TextField', [], {}),
            'follower': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.User']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'organizer': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'subtitle': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'time': ('django.db.models.fields.DateTimeField', [], {}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        'nbg.eventcategory': {
            'Meta': {'object_name': 'EventCategory'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        'nbg.lesson': {
            'Meta': {'object_name': 'Lesson'},
            'course': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['nbg.Course']"}),
            'day': ('django.db.models.fields.SmallIntegerField', [], {}),
            'end': ('django.db.models.fields.SmallIntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'start': ('django.db.models.fields.SmallIntegerField', [], {}),
            'weeks': ('django.db.models.fields.CommaSeparatedIntegerField', [], {'max_length': '200', 'blank': 'True'}),
            'weeks_display': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'weeks_raw': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'weekset': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['nbg.Weekset']", 'null': 'True'})
        },
        'nbg.newsfeed': {
            'Meta': {'object_name': 'NewsFeed'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'info': ('django.db.models.fields.CharField', [], {'max_length': '755', 'null': 'True'}),
            'news_type': ('django.db.models.fields.IntegerField', [], {}),
            'object_id': ('django.db.models.fields.IntegerField', [], {}),
            'ref_model': ('django.db.models.fields.CharField', [], {'max_length': '55'}),
            'time': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'})
        },
        'nbg.room': {
            'Meta': {'object_name': 'Room'},
            'building': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['nbg.Building']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30'})
        },
        'nbg.roomavailability': {
            'Meta': {'object_name': 'RoomAvailability'},
            'availability': ('django.db.models.fields.CommaSeparatedIntegerField', [], {'max_length': '50'}),
            'date': ('django.db.models.fields.DateField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'room': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['nbg.Room']"})
        },
        'nbg.scheduleunit': {
            'Meta': {'object_name': 'ScheduleUnit'},
            'end': ('django.db.models.fields.TimeField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'number': ('django.db.models.fields.SmallIntegerField', [], {}),
            'start': ('django.db.models.fields.TimeField', [], {}),
            'university': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['nbg.University']"})
        },
        'nbg.semester': {
            'Meta': {'object_name': 'Semester'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'university': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['nbg.University']"}),
            'week_end': ('django.db.models.fields.DateField', [], {}),
            'week_start': ('django.db.models.fields.DateField', [], {}),
            'year': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'nbg.university': {
            'Meta': {'object_name': 'University'},
            'english_name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lessons_afternoon': ('django.db.models.fields.SmallIntegerField', [], {}),
            'lessons_evening': ('django.db.models.fields.SmallIntegerField', [], {}),
            'lessons_morning': ('django.db.models.fields.SmallIntegerField', [], {}),
            'lessons_separator': ('django.db.models.fields.CommaSeparatedIntegerField', [], {'max_length': '50'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'support_import_course': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'support_list_course': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'support_ta': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'nbg.useraction': {
            'Meta': {'object_name': 'UserAction'},
            'action_type': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'semester': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['nbg.Semester']"}),
            'time': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'nbg.userprofile': {
            'Meta': {'object_name': 'UserProfile'},
            'campus': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['nbg.Campus']", 'null': 'True'}),
            'courses': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['nbg.Course']", 'symmetrical': 'False', 'through': "orm['nbg.CourseStatus']", 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nickname': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'realname': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'renren_id': ('django.db.models.fields.BigIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'renren_name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'renren_token': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['auth.User']", 'unique': 'True'}),
            'weibo_id': ('django.db.models.fields.BigIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'weibo_name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'weibo_token': ('django.db.models.fields.CharField', [], {'max_length': '32', 'blank': 'True'})
        },
        'nbg.weekset': {
            'Meta': {'object_name': 'Weekset'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'semester': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['nbg.Semester']"}),
            'weeks': ('django.db.models.fields.CommaSeparatedIntegerField', [], {'max_length': '200', 'blank': 'True'})
        },
        'nbg.wiki': {
            'Meta': {'object_name': 'Wiki'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'node': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['nbg.WikiNode']"}),
            'university': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['nbg.University']"})
        },
        'nbg.wikinode': {
            'Meta': {'object_name': 'WikiNode'},
            'content': ('django.db.models.fields.TextField', [], {}),
            'father': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['nbg.WikiNode']", 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '1'})
        }
    }

    complete_apps = ['nbg']