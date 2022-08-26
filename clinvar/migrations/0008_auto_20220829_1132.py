# Generated by Django 3.2.12 on 2022-08-29 11:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("clinvar", "0007_alter_clinvar_details"),
    ]

    operations = [
        migrations.RenameField(
            model_name="clinvar", old_name="point_rating", new_name="gold_stars",
        ),
        migrations.RemoveField(model_name="clinvar", name="pathogenicity_summary",),
        migrations.AddField(
            model_name="clinvar", name="origin", field=models.CharField(max_length=32, null=True),
        ),
        migrations.AddField(
            model_name="clinvar", name="rcv", field=models.CharField(max_length=32, null=True),
        ),
        migrations.AddField(
            model_name="clinvar",
            name="variation_id",
            field=models.CharField(max_length=32, null=True),
        ),
    ]
