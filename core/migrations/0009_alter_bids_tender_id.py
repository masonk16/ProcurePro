# Generated by Django 4.1.4 on 2023-01-11 20:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0008_alter_bids_tender_id"),
    ]

    operations = [
        migrations.AlterField(
            model_name="bids",
            name="tender_id",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="bids",
                to="core.tender",
            ),
        ),
    ]
