# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-12-28 18:00
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion




class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('user_profile', '0001_initial'),
        ('bidding', '0001_initial'),
        ('position', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='waiver',
            name='position',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name='waivers',
                to='position.Position',
            ),
        ),
        migrations.AddField(
            model_name='waiver',
            name='reviewer',
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name='reviewed_waivers',
                to='user_profile.UserProfile',
            ),
        ),
        migrations.AddField(
            model_name='waiver',
            name='user',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name='waivers',
                to='user_profile.UserProfile',
            ),
        ),
        migrations.AddField(
            model_name='userbidstatistics',
            name='bidcycle',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name='user_bid_statistics',
                to='bidding.BidCycle',
            ),
        ),
        migrations.AddField(
            model_name='userbidstatistics',
            name='user',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name='bid_statistics',
                to='user_profile.UserProfile',
            ),
        ),
        migrations.AddField(
            model_name='statussurvey',
            name='bidcycle',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name='status_surveys',
                to='bidding.BidCycle',
            ),
        ),
        migrations.AddField(
            model_name='statussurvey',
            name='user',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name='status_surveys',
                to='user_profile.UserProfile',
            ),
        ),
        migrations.AddField(
            model_name='bidcycle',
            name='positions',
            field=models.ManyToManyField(
                related_name='bid_cycles', to='position.Position'
            ),
        ),
        migrations.AddField(
            model_name='bid',
            name='bidcycle',
            field=models.ForeignKey(
                help_text='The bidcycle for this bid',
                on_delete=django.db.models.deletion.CASCADE,
                related_name='bids',
                to='bidding.BidCycle',
            ),
        ),
        migrations.AddField(
            model_name='bid',
            name='position',
            field=models.ForeignKey(
                help_text='The position this bid is for',
                on_delete=django.db.models.deletion.CASCADE,
                related_name='bids',
                to='position.Position',
            ),
        ),
        migrations.AddField(
            model_name='bid',
            name='reviewer',
            field=models.ForeignKey(
                help_text='The bureau reviewer for this bid',
                null=True,
                on_delete=django.db.models.deletion.DO_NOTHING,
                related_name='reviewing_bids',
                to='user_profile.UserProfile',
            ),
        ),
        migrations.AddField(
            model_name='bid',
            name='user',
            field=models.ForeignKey(
                help_text='The user owning this bid',
                on_delete=django.db.models.deletion.CASCADE,
                related_name='bidlist',
                to='user_profile.UserProfile',
            ),
        ),
        migrations.AlterUniqueTogether(
            name='userbidstatistics', unique_together={('bidcycle', 'user')}
        ),
        migrations.AlterUniqueTogether(
            name='statussurvey', unique_together={('user', 'bidcycle')}
        ),
    ]
