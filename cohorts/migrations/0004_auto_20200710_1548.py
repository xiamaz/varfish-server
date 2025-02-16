# -*- coding: utf-8 -*-
# Generated by Django 1.11.29 on 2020-07-10 15:48
from __future__ import unicode_literals

import uuid

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("cohorts", "0003_auto_20200701_1255"),
    ]

    operations = [
        migrations.AlterField(
            model_name="cohort",
            name="sodar_uuid",
            field=models.UUIDField(default=uuid.uuid4, help_text="Cohort SODAR UUID", unique=True),
        ),
    ]
