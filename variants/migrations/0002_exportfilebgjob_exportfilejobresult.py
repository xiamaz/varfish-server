# -*- coding: utf-8 -*-
# Generated by Django 1.11.16 on 2018-10-26 12:27
from __future__ import unicode_literals

import uuid

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("projectroles", "0005_update_uuid"),
        ("bgjobs", "0002_backgroundjoblogentry"),
        ("variants", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="ExportFileBgJob",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
                    ),
                ),
                (
                    "sodar_uuid",
                    models.UUIDField(default=uuid.uuid4, help_text="Case SODAR UUID", unique=True),
                ),
                (
                    "query_args",
                    models.JSONField(help_text="(Validated) query parameters"),
                ),
                (
                    "file_type",
                    models.CharField(
                        choices=[("tsv", "TSV File"), ("xlsx", "Excel File (XLSX)")],
                        help_text="File types for exported file",
                        max_length=32,
                    ),
                ),
                (
                    "bg_job",
                    models.ForeignKey(
                        help_text="Background job for state etc.",
                        on_delete=django.db.models.deletion.CASCADE,
                        to="bgjobs.BackgroundJob",
                    ),
                ),
                (
                    "case",
                    models.ForeignKey(
                        help_text="The case to export",
                        on_delete=django.db.models.deletion.CASCADE,
                        to="variants.Case",
                    ),
                ),
                (
                    "project",
                    models.ForeignKey(
                        help_text="Project in which this objects belongs",
                        on_delete=django.db.models.deletion.CASCADE,
                        to="projectroles.Project",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="ExportFileJobResult",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
                    ),
                ),
                (
                    "expiry_time",
                    models.DateTimeField(help_text="Time at which the file download expires"),
                ),
                ("payload", models.BinaryField(help_text="Resulting exported file")),
                (
                    "job",
                    models.OneToOneField(
                        help_text="Related file export job",
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="export_result",
                        to="variants.ExportFileBgJob",
                    ),
                ),
            ],
        ),
    ]
