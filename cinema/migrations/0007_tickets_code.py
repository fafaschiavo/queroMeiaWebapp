# -*- coding: utf-8 -*-
# Generated by Django 1.10.dev20160307181939 on 2016-04-10 01:00
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cinema', '0006_auto_20160410_0025'),
    ]

    operations = [
        migrations.AddField(
            model_name='tickets',
            name='code',
            field=models.CharField(default=0, max_length=200),
        ),
    ]