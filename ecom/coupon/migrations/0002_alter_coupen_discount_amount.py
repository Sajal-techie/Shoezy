# Generated by Django 5.0 on 2024-01-19 04:41

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("coupon", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="coupen",
            name="discount_amount",
            field=models.DecimalField(
                decimal_places=2, default=0, max_digits=10, null=True
            ),
        ),
    ]
