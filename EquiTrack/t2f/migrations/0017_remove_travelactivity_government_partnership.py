# -*- coding: utf-8 -*-
# Generated by Django 1.9.10 on 2017-06-08 08:17
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('t2f', '0016_delete_travelpermission'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='travelactivity',
            name='government_partnership',
        ),
    ]
