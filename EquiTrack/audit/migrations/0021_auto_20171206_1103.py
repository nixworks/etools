# -*- coding: utf-8 -*-
# Generated by Django 1.9.10 on 2017-12-06 11:03
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('audit', '0020_auto_20171205_1305'),
    ]

    operations = [
        migrations.AddField(
            model_name='engagement',
            name='agreement1',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='purchase_order.PurchaseOrder', verbose_name='Purchase Order'),
        ),
        migrations.AddField(
            model_name='engagement',
            name='staff_members1',
            field=models.ManyToManyField(null=True, to='purchase_order.AuditorStaffMember', verbose_name='Staff Members'),
        ),
        migrations.AddField(
            model_name='engagement',
            name='po_item1',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='purchase_order.PurchaseOrderItem', verbose_name='PO Item Number'),
        ),
    ]
