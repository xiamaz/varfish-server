# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2019-07-23 09:34
from __future__ import unicode_literals

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("svdbs", "0002_auto_20190619_1529")]

    operations = [
        migrations.AlterField(
            model_name="gnomadsv",
            name="name",
            field=django.contrib.postgres.fields.ArrayField(
                base_field=models.CharField(max_length=64), size=None
            ),
        )
    ]
