# -*- coding: utf-8 -*-
# Generated by Django 1.10.dev20160307181939 on 2016-05-30 22:34
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cinema', '0014_auto_20160513_0422'),
    ]

    operations = [
        migrations.AddField(
            model_name='orders',
            name='payment_request_id',
            field=models.IntegerField(default=0),
        ),
    ]
