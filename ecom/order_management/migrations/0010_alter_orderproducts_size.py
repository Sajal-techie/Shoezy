# Generated by Django 5.0 on 2024-01-04 11:01

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("order_management", "0009_orderproducts_size_alter_orderproducts_product"),
    ]

    operations = [
        migrations.AlterField(
            model_name="orderproducts",
            name="size",
            field=models.IntegerField(),
        ),
    ]
