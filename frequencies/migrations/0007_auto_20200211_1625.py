# -*- coding: utf-8 -*-
# Generated by Django 1.11.25 on 2020-02-11 16:25
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("frequencies", "0006_remove_mtdb_gap"),
    ]

    operations = [
        migrations.RenameField(
            model_name="helixmtdb",
            old_name="ac",
            new_name="ac_hom",
        ),
        migrations.AddField(
            model_name="helixmtdb",
            name="is_triallelic",
            field=models.BooleanField(default=False),
        ),
    ]
