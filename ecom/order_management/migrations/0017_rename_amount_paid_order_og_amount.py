# Generated by Django 5.0 on 2024-01-19 08:59

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("order_management", "0016_rename_amount_payed_order_amount_paid"),
    ]

    operations = [
        migrations.RenameField(
            model_name="order",
            old_name="amount_paid",
            new_name="og_amount",
        ),
    ]
