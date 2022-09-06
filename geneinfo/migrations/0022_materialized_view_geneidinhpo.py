# -*- coding: utf-8 -*-
# Generated by Django 1.11.29 on 2020-07-10 16:03
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models

operations = [
    migrations.CreateModel(
        name="GeneIdInHpo",
        fields=[
            (
                "id",
                models.AutoField(
                    auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
                ),
            ),
            ("entrez_id", models.CharField(max_length=16)),
            ("ensembl_gene_id", models.CharField(max_length=32)),
        ],
        options={"db_table": "geneinfo_geneidinhpo", "managed": settings.IS_TESTING},
    ),
]


if not settings.IS_TESTING:
    operations.append(
        migrations.RunSQL(
            """
            CREATE MATERIALIZED VIEW geneinfo_geneidinhpo
            AS
                SELECT
                    DISTINCT
                    row_number() OVER (PARTITION BY true) AS id,
                    entrez_id,
                    ensembl_gene_id
                FROM geneinfo_hpo
                LEFT OUTER JOIN geneinfo_mim2genemedgen USING (omim_id)
                LEFT OUTER JOIN geneinfo_hgnc USING (entrez_id)
                WHERE entrez_id IS NOT NULL
            WITH DATA;
            CREATE INDEX geneinfo_geneidinhpo_ensembl_gene_id ON geneinfo_geneidinhpo (
                ensembl_gene_id
            );
            CREATE INDEX geneinfo_geneidinhpo_entrez_id ON geneinfo_geneidinhpo (
                entrez_id
            );
            """,
            """
            DROP MATERIALIZED VIEW geneinfo_geneidinhpo;
            """,
        )
    )


class Migration(migrations.Migration):

    dependencies = [
        ("geneinfo", "0021_auto_20200106_1000"),
    ]

    operations = operations
