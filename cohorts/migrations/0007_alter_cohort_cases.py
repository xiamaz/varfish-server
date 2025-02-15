# Generated by Django 3.2.16 on 2023-01-02 13:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("variants", "0091_alter_casephenotypeterms_sodar_uuid"),
        ("cohorts", "0006_auto_20230102_1310"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="cohort",
            name="cases",
        ),
        migrations.AddField(
            model_name="cohort",
            name="cases",
            field=models.ManyToManyField(through="cohorts.CohortCase", to="variants.Case"),
        ),
    ]
