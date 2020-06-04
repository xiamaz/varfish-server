# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2019-04-16 14:00
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


operations = [
    migrations.CreateModel(
        name="ClinvarPathogenicGenes",
        fields=[
            (
                "id",
                models.AutoField(
                    auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
                ),
            ),
            ("symbol", models.CharField(max_length=16)),
            ("entrez_id", models.CharField(max_length=16, null=True)),
            ("ensembl_gene_id", models.CharField(max_length=16, null=True)),
            ("pathogenic_count", models.IntegerField()),
            ("likely_pathogenic_count", models.IntegerField()),
        ],
        options={"db_table": "clinvar_clinvarpathogenicgenes", "managed": settings.IS_TESTING},
    )
]


if not settings.IS_TESTING:
    operations.append(
        migrations.RunSQL(
            """
            CREATE MATERIALIZED VIEW clinvar_clinvarpathogenicgenes
            AS
                SELECT
                    ROW_NUMBER() OVER () AS id,
                    symbol,
                    geneinfo_hgnc.ensembl_gene_id,
                    geneinfo_refseqtohgnc.entrez_id,
                    pathogenic_count,
                    likely_pathogenic_count
                FROM (
                    SELECT
                        unnest(symbols) as symbol,
                        SUM(CASE WHEN pathogenicity = 'pathogenic' THEN 1 ELSE 0 END) AS pathogenic_count,
                        SUM(CASE WHEN pathogenicity = 'likely pathogenic' THEN 1 ELSE 0 END) AS likely_pathogenic_count
                    FROM clinvar_clinvar
                    GROUP BY symbol
                    HAVING
                        SUM(CASE WHEN pathogenicity = 'pathogenic' THEN 1 ELSE 0 END) > 0 OR
                        SUM(CASE WHEN pathogenicity = 'likely pathogenic' THEN 1 ELSE 0 END) > 0
                ) AS clinvar_pathogenic_counts
                LEFT OUTER JOIN geneinfo_hgnc USING (symbol)
                LEFT OUTER JOIN geneinfo_refseqtohgnc USING (hgnc_id)
            WITH DATA;
            """,
            """
            DROP MATERIALIZED VIEW clinvar_clinvarpathogenicgenes;
            """,
        )
    )


class Migration(migrations.Migration):
    dependencies = [
        ("clinvar", "0005_auto_20200611_1719"),
        ("geneinfo", "0005_auto_20190104_1554"),
        ("geneinfo", "0007_refseqtohgnc"),
    ]
    operations = operations
