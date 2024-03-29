# Generated by Django 5.0 on 2024-01-03 11:34

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("cart", "0006_wishlist_stock"),
        ("productmanagement", "0013_productvariant_color"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="cart",
            name="product_id",
        ),
        migrations.RemoveField(
            model_name="wishlist",
            name="product_id",
        ),
        migrations.AddField(
            model_name="cart",
            name="product",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="productmanagement.productvariant",
            ),
        ),
        migrations.AddField(
            model_name="wishlist",
            name="product",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="productmanagement.productvariant",
            ),
        ),
    ]
