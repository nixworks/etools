# -*- coding: utf-8 -*-
# Generated by Django 1.9.10 on 2017-10-13 21:47
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reports', '0013_auto_20170829_1727'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='goal',
            name='sector',
        ),
        migrations.DeleteModel(
            name='Goal',
        ),
    ]
