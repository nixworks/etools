# -*- coding: utf-8 -*-
# Generated by Django 1.9.10 on 2017-06-30 13:03
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('partners', '0030_intervention_signed_pd_document'),
        ('audit', '0003_auto_20170630_0602'),
    ]

    operations = [
        migrations.AddField(
            model_name='engagement',
            name='active_pd',
            field=models.ManyToManyField(to='partners.Intervention', verbose_name='Active PDs'),
        ),
    ]