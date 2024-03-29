# Generated by Django 5.0 on 2023-12-20 14:07

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("productmanagement", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="product",
            name="image1",
            field=models.ImageField(blank=True, upload_to="media/"),
        ),
        migrations.CreateModel(
            name="ProductImages",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("images", models.ImageField(upload_to="media/")),
                (
                    "product",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="images",
                        to="productmanagement.product",
                    ),
                ),
            ],
        ),
    ]
