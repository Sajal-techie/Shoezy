# Generated by Django 5.0 on 2024-01-18 08:55

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("order_management", "0015_alter_order_amount_payed"),
    ]

    operations = [
        migrations.RenameField(
            model_name="order",
            old_name="amount_payed",
            new_name="amount_paid",
        ),
    ]
