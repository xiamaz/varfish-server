# Generated by Django 3.2.12 on 2022-07-01 09:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("svs", "0018_extend_structuralvariant")]

    operations = [
        migrations.AddIndex(
            model_name="backgroundsv",
            index=models.Index(
                fields=["bg_sv_set_id", "release", "chromosome", "bin"],
                name="svs_backgro_bg_sv_s_72b34f_idx",
            ),
        )
    ]
