# Generated by Django 5.0 on 2023-12-30 18:03

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("order_management", "0004_alter_orderproducts_delivery_date"),
    ]

    operations = [
        migrations.AlterField(
            model_name="orderproducts",
            name="delivery_date",
            field=models.DateField(blank=True, null=True),
        ),
    ]
