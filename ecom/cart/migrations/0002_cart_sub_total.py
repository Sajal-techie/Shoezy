# Generated by Django 5.0 on 2023-12-26 13:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='sub_total',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
        ),
    ]