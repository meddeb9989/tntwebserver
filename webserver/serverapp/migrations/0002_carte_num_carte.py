# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-08 16:55
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('serverapp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='carte',
            name='num_carte',
            field=models.BigIntegerField(default=0),
            preserve_default=False,
        ),
    ]
