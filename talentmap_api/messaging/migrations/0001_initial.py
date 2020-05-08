# Generated by Django 2.0.13 on 2020-05-08 15:50

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.TextField(help_text='The message for the notification')),
                ('tags', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=20), default=list, help_text="This notification's tags", size=None)),
                ('is_read', models.BooleanField(default=False, help_text='Whether this notification has been read')),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_updated', models.DateTimeField(auto_now=True)),
            ],
            options={
                'ordering': ['date_updated'],
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Sharable',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sharable_id', models.IntegerField(help_text='The ID of the model instance for this sharable')),
                ('sharable_model', models.TextField(help_text='The string of the model')),
                ('is_read', models.BooleanField(default=False, help_text='Whether this sharable has been read')),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_updated', models.DateTimeField(auto_now=True)),
            ],
            options={
                'ordering': ['date_created'],
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('priority', models.IntegerField(choices=[(0, 'low'), (1, 'medium'), (2, 'high')], default=0)),
                ('tags', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=20), default=list, help_text="This task's tags", size=None)),
                ('title', models.TextField(null=True)),
                ('content', models.TextField(null=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_updated', models.DateTimeField(auto_now=True)),
                ('date_due', models.DateTimeField(null=True)),
                ('date_completed', models.DateTimeField(null=True)),
            ],
            options={
                'ordering': ['priority', 'date_due'],
                'managed': True,
            },
        ),
    ]
