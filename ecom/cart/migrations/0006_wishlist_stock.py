# Generated by Django 5.0 on 2024-01-01 03:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0005_wishlist'),
    ]

    operations = [
        migrations.AddField(
            model_name='wishlist',
            name='stock',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]
