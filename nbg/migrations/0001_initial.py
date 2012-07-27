# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'App'
        db.create_table('nbg_app', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('version_android_beta', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('version_android_stable', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('version_ios_beta', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('version_ios_stable', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('notice_time', self.gf('django.db.models.fields.DateTimeField')()),
            ('notice_content', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('nbg', ['App'])

        # Adding model 'University'
        db.create_table('nbg_university', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('english_name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('latitude', self.gf('django.db.models.fields.DecimalField')(max_digits=10, decimal_places=6)),
            ('longitude', self.gf('django.db.models.fields.DecimalField')(max_digits=10, decimal_places=6)),
            ('support_import_course', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('support_list_course', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('week_start', self.gf('django.db.models.fields.DateField')()),
            ('week_end', self.gf('django.db.models.fields.DateField')()),
            ('excluded', self.gf('django.db.models.fields.CommaSeparatedIntegerField')(max_length=100)),
            ('lessons_morning', self.gf('django.db.models.fields.SmallIntegerField')()),
            ('lessons_afternoon', self.gf('django.db.models.fields.SmallIntegerField')()),
            ('lessons_evening', self.gf('django.db.models.fields.SmallIntegerField')()),
        ))
        db.send_create_signal('nbg', ['University'])

        # Adding model 'UserProfile'
        db.create_table('nbg_userprofile', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['auth.User'], unique=True)),
            ('weibo_token', self.gf('django.db.models.fields.CharField')(max_length=32)),
        ))
        db.send_create_signal('nbg', ['UserProfile'])

        # Adding model 'ScheduleUnit'
        db.create_table('nbg_scheduleunit', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('number', self.gf('django.db.models.fields.SmallIntegerField')()),
            ('start', self.gf('django.db.models.fields.TimeField')()),
            ('end', self.gf('django.db.models.fields.TimeField')()),
            ('university', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['nbg.University'])),
        ))
        db.send_create_signal('nbg', ['ScheduleUnit'])

        # Adding model 'Course'
        db.create_table('nbg_course', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('original_id', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('credit', self.gf('django.db.models.fields.DecimalField')(max_digits=3, decimal_places=1)),
            ('weeks', self.gf('django.db.models.fields.CommaSeparatedIntegerField')(max_length=200)),
        ))
        db.send_create_signal('nbg', ['Course'])

        # Adding model 'Lesson'
        db.create_table('nbg_lesson', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('day', self.gf('django.db.models.fields.SmallIntegerField')()),
            ('start', self.gf('django.db.models.fields.SmallIntegerField')()),
            ('end', self.gf('django.db.models.fields.SmallIntegerField')()),
            ('location', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('course', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['nbg.Course'])),
        ))
        db.send_create_signal('nbg', ['Lesson'])

        # Adding model 'Teacher'
        db.create_table('nbg_teacher', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('course', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['nbg.Course'])),
        ))
        db.send_create_signal('nbg', ['Teacher'])

        # Adding model 'Ta'
        db.create_table('nbg_ta', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('course', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['nbg.Course'])),
        ))
        db.send_create_signal('nbg', ['Ta'])

        # Adding model 'Assignment'
        db.create_table('nbg_assignment', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('course', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['nbg.Course'])),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('due', self.gf('django.db.models.fields.DateTimeField')()),
            ('content', self.gf('django.db.models.fields.TextField')()),
            ('finished', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('last_modified', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal('nbg', ['Assignment'])

        # Adding model 'Comment'
        db.create_table('nbg_comment', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('course', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['nbg.Course'])),
            ('writer', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('time', self.gf('django.db.models.fields.DateTimeField')()),
            ('content', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('nbg', ['Comment'])

        # Adding model 'Building'
        db.create_table('nbg_building', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('university', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['nbg.University'])),
            ('latitude', self.gf('django.db.models.fields.DecimalField')(max_digits=10, decimal_places=6)),
            ('longitude', self.gf('django.db.models.fields.DecimalField')(max_digits=10, decimal_places=6)),
        ))
        db.send_create_signal('nbg', ['Building'])

        # Adding model 'Room'
        db.create_table('nbg_room', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('building', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['nbg.Building'])),
        ))
        db.send_create_signal('nbg', ['Room'])

        # Adding model 'RoomAvailability'
        db.create_table('nbg_roomavailability', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('room', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['nbg.Room'])),
            ('date', self.gf('django.db.models.fields.DateField')()),
            ('availability', self.gf('django.db.models.fields.CommaSeparatedIntegerField')(max_length=50)),
        ))
        db.send_create_signal('nbg', ['RoomAvailability'])

        # Adding model 'EventCategory'
        db.create_table('nbg_eventcategory', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
        ))
        db.send_create_signal('nbg', ['EventCategory'])

        # Adding model 'Event'
        db.create_table('nbg_event', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('subtitle', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('category', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['nbg.EventCategory'])),
            ('time', self.gf('django.db.models.fields.DateTimeField')()),
            ('location', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('organizer', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('content', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('nbg', ['Event'])

        # Adding M2M table for field follower on 'Event'
        db.create_table('nbg_event_follower', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('event', models.ForeignKey(orm['nbg.event'], null=False)),
            ('user', models.ForeignKey(orm['auth.user'], null=False))
        ))
        db.create_unique('nbg_event_follower', ['event_id', 'user_id'])

        # Adding model 'WikiNode'
        db.create_table('nbg_wikinode', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('father', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['nbg.WikiNode'], null=True)),
            ('type', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('content', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('nbg', ['WikiNode'])

        # Adding model 'Wiki'
        db.create_table('nbg_wiki', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('university', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['nbg.University'])),
            ('node', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['nbg.WikiNode'])),
        ))
        db.send_create_signal('nbg', ['Wiki'])


    def backwards(self, orm):
        # Deleting model 'App'
        db.delete_table('nbg_app')

        # Deleting model 'University'
        db.delete_table('nbg_university')

        # Deleting model 'UserProfile'
        db.delete_table('nbg_userprofile')

        # Deleting model 'ScheduleUnit'
        db.delete_table('nbg_scheduleunit')

        # Deleting model 'Course'
        db.delete_table('nbg_course')

        # Deleting model 'Lesson'
        db.delete_table('nbg_lesson')

        # Deleting model 'Teacher'
        db.delete_table('nbg_teacher')

        # Deleting model 'Ta'
        db.delete_table('nbg_ta')

        # Deleting model 'Assignment'
        db.delete_table('nbg_assignment')

        # Deleting model 'Comment'
        db.delete_table('nbg_comment')

        # Deleting model 'Building'
        db.delete_table('nbg_building')

        # Deleting model 'Room'
        db.delete_table('nbg_room')

        # Deleting model 'RoomAvailability'
        db.delete_table('nbg_roomavailability')

        # Deleting model 'EventCategory'
        db.delete_table('nbg_eventcategory')

        # Deleting model 'Event'
        db.delete_table('nbg_event')

        # Removing M2M table for field follower on 'Event'
        db.delete_table('nbg_event_follower')

        # Deleting model 'WikiNode'
        db.delete_table('nbg_wikinode')

        # Deleting model 'Wiki'
        db.delete_table('nbg_wiki')


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
            'due': ('django.db.models.fields.DateTimeField', [], {}),
            'finished': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_modified': ('django.db.models.fields.DateTimeField', [], {}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'nbg.building': {
            'Meta': {'object_name': 'Building'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'latitude': ('django.db.models.fields.DecimalField', [], {'max_digits': '10', 'decimal_places': '6'}),
            'longitude': ('django.db.models.fields.DecimalField', [], {'max_digits': '10', 'decimal_places': '6'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
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
            'credit': ('django.db.models.fields.DecimalField', [], {'max_digits': '3', 'decimal_places': '1'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'original_id': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'weeks': ('django.db.models.fields.CommaSeparatedIntegerField', [], {'max_length': '200'})
        },
        'nbg.event': {
            'Meta': {'object_name': 'Event'},
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['nbg.EventCategory']"}),
            'content': ('django.db.models.fields.TextField', [], {}),
            'follower': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.User']", 'symmetrical': 'False'}),
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
            'start': ('django.db.models.fields.SmallIntegerField', [], {})
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
        'nbg.ta': {
            'Meta': {'object_name': 'Ta'},
            'course': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['nbg.Course']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'nbg.teacher': {
            'Meta': {'object_name': 'Teacher'},
            'course': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['nbg.Course']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'nbg.university': {
            'Meta': {'object_name': 'University'},
            'english_name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'excluded': ('django.db.models.fields.CommaSeparatedIntegerField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'latitude': ('django.db.models.fields.DecimalField', [], {'max_digits': '10', 'decimal_places': '6'}),
            'lessons_afternoon': ('django.db.models.fields.SmallIntegerField', [], {}),
            'lessons_evening': ('django.db.models.fields.SmallIntegerField', [], {}),
            'lessons_morning': ('django.db.models.fields.SmallIntegerField', [], {}),
            'longitude': ('django.db.models.fields.DecimalField', [], {'max_digits': '10', 'decimal_places': '6'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'support_import_course': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'support_list_course': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'week_end': ('django.db.models.fields.DateField', [], {}),
            'week_start': ('django.db.models.fields.DateField', [], {})
        },
        'nbg.userprofile': {
            'Meta': {'object_name': 'UserProfile'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['auth.User']", 'unique': 'True'}),
            'weibo_token': ('django.db.models.fields.CharField', [], {'max_length': '32'})
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