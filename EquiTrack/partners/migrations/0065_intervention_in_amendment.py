# -*- coding: utf-8 -*-
# Generated by Django 1.9.10 on 2018-01-17 19:04
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('partners', '0064_auto_20180110_1505'),
    ]

    operations = [
        migrations.AddField(
            model_name='intervention',
            name='in_amendment',
            field=models.BooleanField(default=False, verbose_name='Amendment Open'),
        ),
    ]