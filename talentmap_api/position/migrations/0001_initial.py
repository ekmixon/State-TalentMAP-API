# Generated by Django 2.0.13 on 2020-09-25 15:19

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Classification',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('_string_representation', models.CharField(blank=True, help_text='The string representation of this object', max_length=255, null=True)),
                ('code', models.CharField(db_index=True, help_text='The classification code', max_length=255, unique=True)),
                ('description', models.CharField(help_text='Text description of the classification', max_length=255)),
            ],
            options={
                'ordering': ['code'],
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Grade',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('_string_representation', models.CharField(blank=True, help_text='The string representation of this object', max_length=255, null=True)),
                ('code', models.CharField(db_index=True, max_length=255, unique=True)),
                ('rank', models.IntegerField(default=0)),
            ],
            options={
                'ordering': ['rank'],
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Skill',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('_string_representation', models.CharField(blank=True, help_text='The string representation of this object', max_length=255, null=True)),
                ('code', models.CharField(db_index=True, help_text='4 character string code representation of the job skill', max_length=255, unique=True)),
                ('description', models.CharField(help_text='Text description of the job skill', max_length=255)),
            ],
            options={
                'ordering': ['code'],
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='SkillCone',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('_string_representation', models.CharField(blank=True, help_text='The string representation of this object', max_length=255, null=True)),
                ('name', models.CharField(db_index=True, help_text='The name of the skill cone', max_length=255)),
                ('_id', models.TextField(null=True)),
                ('_skill_codes', models.TextField(blank=True, default='', null=True)),
            ],
            options={
                'ordering': ['name'],
                'managed': True,
            },
        ),
    ]
