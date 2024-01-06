# Generated by Django 5.0 on 2024-01-02 11:49

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('productmanagement', '0009_productvariant'),
    ]

    operations = [
        migrations.CreateModel(
            name='Product_Variant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('size', models.CharField(blank=True, choices=[(7, '7'), (8, '8'), (9, '9'), (10, '10')], default='7', max_length=5, null=True)),
                ('stock', models.PositiveIntegerField(blank=True, default=0, null=True)),
                ('product_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='productmanagement.product')),
            ],
        ),
    ]