# -*- coding: utf-8 -*-
# Generated by Django 1.9.10 on 2017-01-12 18:51
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('partners', '0008_auto_20170110_2245'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='gwpcalocation',
            name='governorate',
        ),
        migrations.RemoveField(
            model_name='gwpcalocation',
            name='locality',
        ),
        migrations.RemoveField(
            model_name='gwpcalocation',
            name='region',
        ),
    ]