# Generated by Django 5.0 on 2023-12-31 07:01

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("productmanagement", "0004_product_is_listed"),
    ]

    operations = [
        migrations.AddField(
            model_name="product",
            name="discount_percentage",
            field=models.PositiveIntegerField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name="product",
            name="description",
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="product",
            name="quantity",
            field=models.PositiveIntegerField(default=0),
        ),
    ]
