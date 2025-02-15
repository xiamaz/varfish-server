# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2019-05-17 11:26
from __future__ import unicode_literals

import uuid

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("variants", "0038_auto_20190507_1155"),
    ]

    operations = [
        migrations.CreateModel(
            name="AcmgCriteriaRating",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
                    ),
                ),
                (
                    "date_created",
                    models.DateTimeField(auto_now_add=True, help_text="DateTime of creation"),
                ),
                (
                    "date_modified",
                    models.DateTimeField(auto_now=True, help_text="DateTime of last modification"),
                ),
                (
                    "sodar_uuid",
                    models.UUIDField(default=uuid.uuid4, help_text="Case SODAR UUID", unique=True),
                ),
                ("release", models.CharField(max_length=32)),
                ("chromosome", models.CharField(max_length=32)),
                ("position", models.IntegerField()),
                ("reference", models.CharField(max_length=512)),
                ("alternative", models.CharField(max_length=512)),
                (
                    "pvs1",
                    models.IntegerField(
                        default=False,
                        help_text=(
                            "null variant (nonsense, frameshift, canonical ±1 or 2 splice sites, initiation codon, single or multiexon deletion) in a gene where LOF is a known mechanism of disease",
                        ),
                        verbose_name="PVS1",
                    ),
                ),
                (
                    "ps1",
                    models.IntegerField(
                        default=0,
                        help_text="Same amino acid change as a previously established pathogenic variant regardless of nucleotide change",
                        verbose_name="PS1",
                    ),
                ),
                (
                    "ps2",
                    models.IntegerField(
                        default=0,
                        help_text="De novo (both maternity and paternity confirmed) in a patient with the disease and no family history",
                        verbose_name="PS2",
                    ),
                ),
                (
                    "ps3",
                    models.IntegerField(
                        default=0,
                        help_text="Well-established in vitro or in vivo functional studies supportive of a damaging effect on the gene or gene product",
                        verbose_name="PS3",
                    ),
                ),
                (
                    "ps4",
                    models.IntegerField(
                        default=0,
                        help_text="The prevalence of the variant in affected individuals is significantly increased compared with the prevalence in controls",
                        verbose_name="PS4",
                    ),
                ),
                (
                    "pm1",
                    models.IntegerField(
                        default=0,
                        help_text="Located in a mutational hot spot and/or critical and well-established functional domain (e.g., active site of an enzyme) without benign variation",
                        verbose_name="PM1",
                    ),
                ),
                (
                    "pm2",
                    models.IntegerField(
                        default=0,
                        help_text="Absent from controls (or at extremely low frequency if recessive) in Exome Sequencing Project, 1000 Genomes Project, or Exome Aggregation Consortium",
                        verbose_name="PM2",
                    ),
                ),
                (
                    "pm3",
                    models.IntegerField(
                        default=0,
                        help_text="For recessive disorders, detected in trans with a pathogenic variant",
                        verbose_name="PM3",
                    ),
                ),
                (
                    "pm4",
                    models.IntegerField(
                        default=0,
                        help_text="Protein length changes as a result of in-frame deletions/insertions in a nonrepeat region or stop-loss variants",
                        verbose_name="PM4",
                    ),
                ),
                (
                    "pm5",
                    models.IntegerField(
                        default=0,
                        help_text="Novel missense change at an amino acid residue where a different missense change determined to be pathogenic has been seen before",
                        verbose_name="PM5",
                    ),
                ),
                (
                    "pm6",
                    models.IntegerField(
                        default=0,
                        help_text="Assumed de novo, but without confirmation of paternity and maternity",
                        verbose_name="PM6",
                    ),
                ),
                (
                    "pp1",
                    models.IntegerField(
                        default=0,
                        help_text="Cosegregation with disease in multiple affected family members in a gene definitively known to cause the disease",
                        verbose_name="PP1",
                    ),
                ),
                (
                    "pp2",
                    models.IntegerField(
                        default=0,
                        help_text="Missense variant in a gene that has a low rate of benign missense variation and in which missense variants are: a common mechanism of disease",
                        verbose_name="PP2",
                    ),
                ),
                (
                    "pp3",
                    models.IntegerField(
                        default=0,
                        help_text="Multiple lines of computational evidence support a deleterious effect on the gene or gene product (conservation, evolutionary, splicing impact, etc.)",
                        verbose_name="PP3",
                    ),
                ),
                (
                    "pp4",
                    models.IntegerField(
                        default=0,
                        help_text="Patient's phenotype or family history is highly specific for a disease with a single genetic etiology",
                        verbose_name="PP4",
                    ),
                ),
                (
                    "pp5",
                    models.IntegerField(
                        default=0,
                        help_text="Reputable source recently reports variant as pathogenic, but the evidence is not available to the laboratory to perform an independent evaluation",
                        verbose_name="PP5",
                    ),
                ),
                (
                    "ba1",
                    models.IntegerField(
                        default=0,
                        help_text="Allele frequency is >5% in Exome Sequencing Project, 1000 Genomes Project, or Exome Aggregation Consortium",
                        verbose_name="BA1",
                    ),
                ),
                (
                    "bs1",
                    models.IntegerField(
                        default=0,
                        help_text="Allele frequency is greater than expected for disorder (see Table 6)",
                        verbose_name="BS1",
                    ),
                ),
                (
                    "bs2",
                    models.IntegerField(
                        default=0,
                        help_text="Observed in a healthy adult individual for a recessive (homozygous), dominant (heterozygous), or X-linked (hemizygous) disorder, with full penetrance expected at an early age",
                        verbose_name="BS2",
                    ),
                ),
                (
                    "bs3",
                    models.IntegerField(
                        default=0,
                        help_text="Well-established in vitro or in vivo functional studies show no damaging effect on protein function or splicing",
                        verbose_name="BS3",
                    ),
                ),
                (
                    "bs4",
                    models.IntegerField(
                        default=0,
                        help_text="BS4: Lack of segregation in affected members of a family",
                        verbose_name="BS4",
                    ),
                ),
                (
                    "bp1",
                    models.IntegerField(
                        default=0,
                        help_text="Missense variant in a gene for which primarily truncating variants are known to cause disease",
                        verbose_name="BP1",
                    ),
                ),
                (
                    "bp2",
                    models.IntegerField(
                        default=0,
                        help_text="Observed in trans with a pathogenic variant for a fully penetrant dominant gene/disorder or observed in cis with a pathogenic variant in any inheritance pattern",
                        verbose_name="BP2",
                    ),
                ),
                (
                    "bp3",
                    models.IntegerField(
                        default=0,
                        help_text="In-frame deletions/insertions in a repetitive region without a known function",
                        verbose_name="BP3",
                    ),
                ),
                (
                    "bp4",
                    models.IntegerField(
                        default=0,
                        help_text="Multiple lines of computational evidence suggest no impact on gene or gene product (conservation, evolutionary, splicing impact, etc.)",
                        verbose_name="BP4",
                    ),
                ),
                (
                    "bp5",
                    models.IntegerField(
                        default=0,
                        help_text="Variant found in a case with an alternate molecular basis for disease",
                        verbose_name="BP5",
                    ),
                ),
                (
                    "bp6",
                    models.IntegerField(
                        default=0,
                        help_text="Reputable source recently reports variant as benign, but the evidence is not available to the laboratory to perform an independent evaluation",
                        verbose_name="BP6",
                    ),
                ),
                (
                    "bp7",
                    models.IntegerField(
                        default=0,
                        help_text="A synonymous (silent) variant for which splicing prediction algorithms predict no impact to the splice consensus sequence nor the creation of a new splice site AND the nucleotide is not highly conserved",
                        verbose_name="BP7",
                    ),
                ),
                (
                    "class_auto",
                    models.IntegerField(
                        blank=True,
                        default=None,
                        help_text="Result of the ACMG classification",
                        null=True,
                        verbose_name="ACMG Classification",
                    ),
                ),
                (
                    "class_override",
                    models.IntegerField(
                        blank=True,
                        default=None,
                        help_text="Use this field to override the auto-computed class assignment",
                        null=True,
                        verbose_name="Class Override",
                    ),
                ),
                (
                    "case",
                    models.ForeignKey(
                        help_text="Case that this rating was given for",
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="acmg_ratings",
                        to="variants.Case",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        blank=True,
                        help_text="User creating the original rating",
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="acmg_ratings",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        )
    ]
