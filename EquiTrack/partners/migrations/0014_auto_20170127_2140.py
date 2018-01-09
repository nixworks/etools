# -*- coding: utf-8 -*-
# Generated by Django 1.9.10 on 2017-01-27 19:40
from __future__ import unicode_literals

import django.contrib.postgres.fields
from django.db import migrations, models


def reverse(apps, schema_editor):
    pass

def agr_copy_type_tmp(apps, schema_editor):
    AgreementAmendment = apps.get_model('partners', 'AgreementAmendment')
    for amd in AgreementAmendment.objects.all():
        amd.tmp_type = amd.type
        amd.save()
        print('saved amd {}'.format(amd.id))

def agr_copy_tmp_arr_type(apps, schema_editor):
    AgreementAmendment = apps.get_model('partners', 'AgreementAmendment')
    amendments = AgreementAmendment.objects.all()
    for amd in amendments:
        amd.type = [amd.tmp_type]
        amd.save()
        print('saved amd {}'.format(amd.id))


class Migration(migrations.Migration):

    dependencies = [
        ('partners', '0013_auto_20170127_0106'),
    ]

    operations = [
        migrations.AddField(
            model_name='agreementamendment',
            name='tmp_type',
            field=models.CharField(blank=True,
                                   choices=[(b'Change IP name', b'Change in Legal Name of Implementing Partner'),
                                            (b'CP extension', b'Extension of Country Programme Cycle'),
                                            (b'Change authorized officer', b'Change Authorized Officer'),
                                            (b'Change banking info', b'Banking Information'),
                                            (b'Additional clause', b'Additional Clause'),
                                            (b'Amend existing clause', b'Amend Existing Clause')], max_length=64,
                                   null=True),
        ),
        migrations.RunPython(
            agr_copy_type_tmp, reverse_code=reverse
        ),
        migrations.RemoveField(
            model_name='agreementamendment',
            name='type',
        ),
        migrations.AddField(
            model_name='agreementamendment',
            name='type',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(
                choices=[(b'Change IP name', b'Change in Legal Name of Implementing Partner'),
                         (b'CP extension', b'Extension of Country Programme Cycle'),
                         (b'Change authorized officer', b'Change Authorized Officer'),
                         (b'Change banking info', b'Banking Information'), (b'Additional clause', b'Additional Clause'),
                         (b'Amend existing clause', b'Amend Existing Clause')], max_length=64), null=True, size=None),
        ),
        migrations.RunPython(
            agr_copy_tmp_arr_type, reverse_code=reverse
        ),

    ]
