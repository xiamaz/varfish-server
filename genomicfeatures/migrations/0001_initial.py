# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2019-04-23 09:40
from __future__ import unicode_literals

import uuid

import django.contrib.postgres.fields
import django.contrib.postgres.indexes
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [("variants", "0005_load_btree_gin_extension")]

    operations = [
        migrations.CreateModel(
            name="EnsemblRegulatoryFeature",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
                    ),
                ),
                (
                    "sodar_uuid",
                    models.UUIDField(
                        default=uuid.uuid4, help_text="Interval set UUID", unique=True
                    ),
                ),
                ("bin", models.IntegerField()),
                (
                    "containing_bins",
                    django.contrib.postgres.fields.ArrayField(
                        base_field=models.IntegerField(), size=None
                    ),
                ),
                (
                    "release",
                    models.CharField(help_text="Genome release of coordinates", max_length=32),
                ),
                ("chromosome", models.CharField(help_text="Chromosome of interval", max_length=32)),
                ("start", models.IntegerField(help_text="1-based start position of interval")),
                ("end", models.IntegerField(help_text="end position of interval")),
                (
                    "stable_id",
                    models.CharField(help_text="ENSR ID of regulatory feature", max_length=32),
                ),
                ("feature_type", models.CharField(help_text="Short feature type", max_length=64)),
                (
                    "feature_type_description",
                    models.CharField(help_text="Feature type description", max_length=128),
                ),
                (
                    "so_term_accession",
                    models.CharField(help_text="SO term accession", max_length=64),
                ),
                ("so_term_name", models.CharField(help_text="SO term name", max_length=256)),
            ],
            options={"abstract": False},
        ),
        migrations.CreateModel(
            name="GeneInterval",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
                    ),
                ),
                (
                    "sodar_uuid",
                    models.UUIDField(
                        default=uuid.uuid4, help_text="Interval set UUID", unique=True
                    ),
                ),
                ("bin", models.IntegerField()),
                (
                    "containing_bins",
                    django.contrib.postgres.fields.ArrayField(
                        base_field=models.IntegerField(), size=None
                    ),
                ),
                (
                    "release",
                    models.CharField(help_text="Genome release of coordinates", max_length=32),
                ),
                ("chromosome", models.CharField(help_text="Chromosome of interval", max_length=32)),
                ("start", models.IntegerField(help_text="1-based start position of interval")),
                ("end", models.IntegerField(help_text="end position of interval")),
                ("database", models.CharField(max_length=128)),
                ("gene_id", models.CharField(max_length=128)),
            ],
        ),
        migrations.CreateModel(
            name="TadBoundaryInterval",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
                    ),
                ),
                (
                    "sodar_uuid",
                    models.UUIDField(
                        default=uuid.uuid4, help_text="Interval set UUID", unique=True
                    ),
                ),
                ("bin", models.IntegerField()),
                (
                    "containing_bins",
                    django.contrib.postgres.fields.ArrayField(
                        base_field=models.IntegerField(), size=None
                    ),
                ),
                (
                    "release",
                    models.CharField(help_text="Genome release of coordinates", max_length=32),
                ),
                ("chromosome", models.CharField(help_text="Chromosome of interval", max_length=32)),
                ("start", models.IntegerField(help_text="1-based start position of interval")),
                ("end", models.IntegerField(help_text="end position of interval")),
            ],
            options={"abstract": False},
        ),
        migrations.CreateModel(
            name="TadInterval",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
                    ),
                ),
                (
                    "sodar_uuid",
                    models.UUIDField(
                        default=uuid.uuid4, help_text="Interval set UUID", unique=True
                    ),
                ),
                ("bin", models.IntegerField()),
                (
                    "containing_bins",
                    django.contrib.postgres.fields.ArrayField(
                        base_field=models.IntegerField(), size=None
                    ),
                ),
                (
                    "release",
                    models.CharField(help_text="Genome release of coordinates", max_length=32),
                ),
                ("chromosome", models.CharField(help_text="Chromosome of interval", max_length=32)),
                ("start", models.IntegerField(help_text="1-based start position of interval")),
                ("end", models.IntegerField(help_text="end position of interval")),
            ],
            options={"abstract": False},
        ),
        migrations.CreateModel(
            name="TadSet",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
                    ),
                ),
                (
                    "sodar_uuid",
                    models.UUIDField(
                        default=uuid.uuid4, help_text="Interval set UUID", unique=True
                    ),
                ),
                (
                    "release",
                    models.CharField(
                        help_text="Genome release for interval set coordinates", max_length=32
                    ),
                ),
                (
                    "name",
                    models.CharField(
                        help_text="Name of the interval set", max_length=32, unique=True
                    ),
                ),
                (
                    "version",
                    models.CharField(help_text="Version of the interval set", max_length=32),
                ),
                (
                    "title",
                    models.TextField(help_text="Name of the interval as displayed to the user"),
                ),
                (
                    "comment",
                    models.TextField(
                        blank=True,
                        help_text="Name of the interval as displayed to the user",
                        null=True,
                    ),
                ),
            ],
            options={"ordering": ["title"]},
        ),
        migrations.CreateModel(
            name="VistaEnhancer",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
                    ),
                ),
                (
                    "sodar_uuid",
                    models.UUIDField(
                        default=uuid.uuid4, help_text="Interval set UUID", unique=True
                    ),
                ),
                ("bin", models.IntegerField()),
                (
                    "containing_bins",
                    django.contrib.postgres.fields.ArrayField(
                        base_field=models.IntegerField(), size=None
                    ),
                ),
                (
                    "release",
                    models.CharField(help_text="Genome release of coordinates", max_length=32),
                ),
                ("chromosome", models.CharField(help_text="Chromosome of interval", max_length=32)),
                ("start", models.IntegerField(help_text="1-based start position of interval")),
                ("end", models.IntegerField(help_text="end position of interval")),
                ("element_id", models.CharField(help_text="enhancer name", max_length=32)),
                (
                    "validation_result",
                    models.CharField(
                        choices=[("positive", "positive"), ("negative", "negative")],
                        help_text="Validation result",
                        max_length=16,
                    ),
                ),
            ],
            options={"abstract": False},
        ),
        migrations.AddIndex(
            model_name="vistaenhancer",
            index=models.Index(
                fields=["release", "chromosome", "bin"], name="genomicfeat_release_e3899e_idx"
            ),
        ),
        migrations.AddIndex(
            model_name="vistaenhancer",
            index=django.contrib.postgres.indexes.GinIndex(
                fields=["release", "chromosome", "containing_bins"],
                name="genomicfeat_release_d51359_gin",
            ),
        ),
        migrations.AlterUniqueTogether(name="tadset", unique_together=set([("name", "version")])),
        migrations.AddField(
            model_name="tadinterval",
            name="tad_set",
            field=models.ForeignKey(
                help_text="The TAD set this TAD belong to",
                on_delete=django.db.models.deletion.CASCADE,
                related_name="tads",
                to="genomicfeatures.TadSet",
            ),
        ),
        migrations.AddField(
            model_name="tadboundaryinterval",
            name="tad_set",
            field=models.ForeignKey(
                help_text="The TAD set this boundary belongs to",
                on_delete=django.db.models.deletion.CASCADE,
                related_name="boundaries",
                to="genomicfeatures.TadSet",
            ),
        ),
        migrations.AddIndex(
            model_name="geneinterval",
            index=models.Index(
                fields=["database", "release", "chromosome", "bin"],
                name="genomicfeat_databas_9e9301_idx",
            ),
        ),
        migrations.AddIndex(
            model_name="geneinterval",
            index=django.contrib.postgres.indexes.GinIndex(
                fields=["database", "release", "chromosome", "containing_bins"],
                name="genomicfeat_databas_a312b0_gin",
            ),
        ),
        migrations.AddIndex(
            model_name="ensemblregulatoryfeature",
            index=models.Index(
                fields=["release", "chromosome", "bin"], name="genomicfeat_release_87d7b8_idx"
            ),
        ),
        migrations.AddIndex(
            model_name="ensemblregulatoryfeature",
            index=django.contrib.postgres.indexes.GinIndex(
                fields=["release", "chromosome", "containing_bins"],
                name="genomicfeat_release_3adf69_gin",
            ),
        ),
        migrations.AddIndex(
            model_name="tadinterval",
            index=models.Index(
                fields=["release", "chromosome", "bin"], name="genomicfeat_release_bef485_idx"
            ),
        ),
        migrations.AddIndex(
            model_name="tadinterval",
            index=django.contrib.postgres.indexes.GinIndex(
                fields=["release", "chromosome", "containing_bins"],
                name="genomicfeat_release_a530cc_gin",
            ),
        ),
        migrations.AddIndex(
            model_name="tadboundaryinterval",
            index=models.Index(
                fields=["release", "chromosome", "bin"], name="genomicfeat_release_472cf6_idx"
            ),
        ),
        migrations.AddIndex(
            model_name="tadboundaryinterval",
            index=django.contrib.postgres.indexes.GinIndex(
                fields=["release", "chromosome", "containing_bins"],
                name="genomicfeat_release_63da73_gin",
            ),
        ),
    ]
