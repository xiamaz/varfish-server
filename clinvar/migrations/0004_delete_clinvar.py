# -*- coding: utf-8 -*-
# Generated by Django 1.11.29 on 2020-06-10 11:45
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("clinvar", "0003_auto_20190619_1636"),
    ]

    operations = [
        migrations.DeleteModel(
            name="Clinvar",
        ),
        migrations.DeleteModel(
            name="ClinvarPathogenicGenes",
        ),
    ]
