# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-20 15:59
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('language', '0002_auto_20170616_1908'),
    ]

    operations = [
        migrations.AlterField(
            model_name='language',
            name='code',
            field=models.CharField(db_index=True, help_text='The two letter code representation of the language', max_length=2, unique=True),
        ),
        migrations.AlterField(
            model_name='proficiency',
            name='code',
            field=models.CharField(help_text='The code representing the linguistic proficiency', max_length=2, unique=True),
        ),
    ]
