# -*- coding: utf-8 -*-
# Generated by Django 1.11.17 on 2019-04-05 15:11
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scrumboard', '0003_auto_20190405_2054'),
    ]

    operations = [
        migrations.AlterField(
            model_name='list',
            name='name',
            field=models.CharField(max_length=50),
        ),
    ]
