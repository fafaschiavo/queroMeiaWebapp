# -*- coding: utf-8 -*-
# Generated by Django 1.10.dev20160307181939 on 2016-04-26 22:35
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cinema', '0009_orders_product_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='bad_requests',
            name='problem_type',
            field=models.CharField(default=0, max_length=200),
        ),
    ]
