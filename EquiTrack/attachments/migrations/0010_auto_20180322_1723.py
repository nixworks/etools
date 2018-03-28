# -*- coding: utf-8 -*-
# Generated by Django 1.10.8 on 2018-03-22 17:23
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('attachments', '0009_auto_20180321_1423'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attachmentflat',
            name='attachment',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='denormalized', to='attachments.Attachment'),
        ),
    ]