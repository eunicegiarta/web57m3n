# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'CoachUser'
        db.create_table('uap_app_coachuser', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['auth.User'], unique=True)),
            ('phone', self.gf('django.db.models.fields.CharField')(max_length=11)),
            ('ee_help', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('cs_help', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('projects_assigned', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('uap_app', ['CoachUser'])

        # Adding model 'TuteeUser'
        db.create_table('uap_app_tuteeuser', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['auth.User'], unique=True)),
            ('phone', self.gf('django.db.models.fields.CharField')(max_length=11)),
            ('ee_request', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('cs_request', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('area_of_interest', self.gf('django.db.models.fields.TextField')()),
            ('research_advisor', self.gf('django.db.models.fields.TextField')()),
            ('research_advisor_email', self.gf('django.db.models.fields.TextField')()),
            ('open_project', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('uap_app', ['TuteeUser'])

        # Adding model 'AdminUser'
        db.create_table('uap_app_adminuser', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['auth.User'], unique=True)),
        ))
        db.send_create_signal('uap_app', ['AdminUser'])

        # Adding model 'Project'
        db.create_table('uap_app_project', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('expiry_date', self.gf('django.db.models.fields.DateTimeField')(null=True)),
            ('status', self.gf('django.db.models.fields.IntegerField')()),
            ('tutee', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['uap_app.TuteeUser'])),
            ('coach', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['uap_app.CoachUser'], null=True)),
            ('video', self.gf('django.db.models.fields.files.FileField')(max_length=100, null=True)),
            ('meeting_details', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal('uap_app', ['Project'])

        # Adding model 'ReassignNote'
        db.create_table('uap_app_reassignnote', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('project', self.gf('django.db.models.fields.related.OneToOneField')(related_name='reassigned_note', unique=True, to=orm['uap_app.Project'])),
            ('details', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('coach', self.gf('django.db.models.fields.related.ForeignKey')(related_name='reassigned_note', to=orm['uap_app.CoachUser'])),
        ))
        db.send_create_signal('uap_app', ['ReassignNote'])


    def backwards(self, orm):
        # Deleting model 'CoachUser'
        db.delete_table('uap_app_coachuser')

        # Deleting model 'TuteeUser'
        db.delete_table('uap_app_tuteeuser')

        # Deleting model 'AdminUser'
        db.delete_table('uap_app_adminuser')

        # Deleting model 'Project'
        db.delete_table('uap_app_project')

        # Deleting model 'ReassignNote'
        db.delete_table('uap_app_reassignnote')


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
        'uap_app.adminuser': {
            'Meta': {'object_name': 'AdminUser'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['auth.User']", 'unique': 'True'})
        },
        'uap_app.coachuser': {
            'Meta': {'object_name': 'CoachUser'},
            'cs_help': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'ee_help': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '11'}),
            'projects_assigned': ('django.db.models.fields.IntegerField', [], {}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['auth.User']", 'unique': 'True'})
        },
        'uap_app.project': {
            'Meta': {'object_name': 'Project'},
            'coach': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['uap_app.CoachUser']", 'null': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'expiry_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'meeting_details': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'status': ('django.db.models.fields.IntegerField', [], {}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'tutee': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['uap_app.TuteeUser']"}),
            'video': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True'})
        },
        'uap_app.reassignnote': {
            'Meta': {'object_name': 'ReassignNote'},
            'coach': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'reassigned_note'", 'to': "orm['uap_app.CoachUser']"}),
            'details': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'project': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'reassigned_note'", 'unique': 'True', 'to': "orm['uap_app.Project']"})
        },
        'uap_app.tuteeuser': {
            'Meta': {'object_name': 'TuteeUser'},
            'area_of_interest': ('django.db.models.fields.TextField', [], {}),
            'cs_request': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'ee_request': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'open_project': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '11'}),
            'research_advisor': ('django.db.models.fields.TextField', [], {}),
            'research_advisor_email': ('django.db.models.fields.TextField', [], {}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['auth.User']", 'unique': 'True'})
        }
    }

    complete_apps = ['uap_app']