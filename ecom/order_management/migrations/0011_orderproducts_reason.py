# Generated by Django 5.0 on 2024-01-06 06:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order_management', '0010_alter_orderproducts_size'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderproducts',
            name='reason',
            field=models.TextField(default='Bought it from offline'),
        ),
    ]
