# Generated by Django 5.0 on 2024-01-18 08:53

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("order_management", "0014_alter_order_amount_payed"),
    ]

    operations = [
        migrations.AlterField(
            model_name="order",
            name="amount_payed",
            field=models.FloatField(blank=True, null=True),
        ),
    ]
