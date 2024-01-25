# Generated by Django 5.0 on 2023-12-31 07:17

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("productmanagement", "0005_product_discount_percentage_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="product",
            name="discount_percentage",
            field=models.DecimalField(
                blank=True, decimal_places=0, default=0, max_digits=3, null=True
            ),
        ),
    ]
