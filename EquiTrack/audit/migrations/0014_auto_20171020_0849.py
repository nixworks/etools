# -*- coding: utf-8 -*-
# Generated by Django 1.9.10 on 2017-10-20 08:49
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('audit', '0013_merge'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='specialauditrecommendation',
            name='number',
        ),
        migrations.RemoveField(
            model_name='specificprocedure',
            name='number',
        ),
    ]