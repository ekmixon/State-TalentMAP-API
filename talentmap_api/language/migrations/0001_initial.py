# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-12-28 18:00
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion




class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Language',
            fields=[
                (
                    'id',
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name='ID',
                    ),
                ),
                (
                    '_string_representation',
                    models.TextField(
                        blank=True,
                        help_text='The string representation of this object',
                        null=True,
                    ),
                ),
                (
                    'code',
                    models.TextField(
                        db_index=True,
                        help_text='The code representation of the language',
                        unique=True,
                    ),
                ),
                (
                    'long_description',
                    models.TextField(
                        help_text='Long-format description of the language, typically the name'
                    ),
                ),
                (
                    'short_description',
                    models.TextField(
                        help_text='Short-format description of the language, typically the name'
                    ),
                ),
                (
                    'effective_date',
                    models.DateField(
                        help_text='The date after which the language is in effect'
                    ),
                ),
            ],
            options={
                'ordering': ['code'],
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Proficiency',
            fields=[
                (
                    'id',
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name='ID',
                    ),
                ),
                (
                    '_string_representation',
                    models.TextField(
                        blank=True,
                        help_text='The string representation of this object',
                        null=True,
                    ),
                ),
                (
                    'code',
                    models.TextField(
                        help_text='The code representing the linguistic proficiency',
                        unique=True,
                    ),
                ),
                (
                    'description',
                    models.TextField(
                        help_text='Text describing the level of proficiency'
                    ),
                ),
            ],
            options={
                'ordering': ['code'],
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Qualification',
            fields=[
                (
                    'id',
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name='ID',
                    ),
                ),
                (
                    '_string_representation',
                    models.TextField(
                        blank=True,
                        help_text='The string representation of this object',
                        null=True,
                    ),
                ),
                (
                    'language',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name='qualifications',
                        to='language.Language',
                    ),
                ),
                (
                    'reading_proficiency',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name='reading_qualifications',
                        to='language.Proficiency',
                    ),
                ),
                (
                    'spoken_proficiency',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name='spoken_qualifications',
                        to='language.Proficiency',
                    ),
                ),
            ],
            options={
                'ordering': ['language__code'],
                'managed': True,
            },
        ),
        migrations.AlterUniqueTogether(
            name='qualification',
            unique_together={
                ('language', 'reading_proficiency', 'spoken_proficiency')
            },
        ),
    ]
