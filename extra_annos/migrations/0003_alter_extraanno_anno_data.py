# Generated by Django 3.2.4 on 2021-06-17 14:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("extra_annos", "0002_auto_20200714_1411"),
    ]

    operations = [
        migrations.AlterField(
            model_name="extraanno",
            name="anno_data",
            field=models.JSONField(default=dict),
        ),
    ]
