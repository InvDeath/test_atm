# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-03-12 18:45
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('atm', '0002_auto_20160310_1753'),
    ]

    operations = [
        migrations.AlterField(
            model_name='card',
            name='number',
            field=models.CharField(max_length=19, unique=True),
        ),
    ]