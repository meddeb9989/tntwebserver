# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-19 22:06
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('serverapp', '0004_auto_20170318_1017'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='confirmed',
            field=models.BooleanField(default=True),
        ),
    ]
