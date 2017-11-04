# -*- coding: utf-8 -*-
# Generated by Django 1.9.10 on 2017-11-04 09:58
from __future__ import unicode_literals

import attachments.models
from django.db import migrations, models
import utils.files.storage


class Migration(migrations.Migration):

    dependencies = [
        ('attachments', '0003_filetype_label'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attachment',
            name='file',
            field=models.FileField(blank=True, null=True, storage=utils.files.storage.SaveNameDefaultStorage(), upload_to=attachments.models.generate_file_path),
        ),
    ]