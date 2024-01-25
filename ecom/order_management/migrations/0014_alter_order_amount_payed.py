# Generated by Django 5.0 on 2024-01-18 08:52

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("order_management", "0013_order_amount_payed_order_coupen_applied_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="order",
            name="amount_payed",
            field=models.FloatField(
                blank=True,
                default=models.DecimalField(
                    blank=True, decimal_places=2, default=0.0, max_digits=10, null=True
                ),
                null=True,
            ),
        ),
    ]
