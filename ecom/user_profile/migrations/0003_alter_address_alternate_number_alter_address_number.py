# Generated by Django 5.0 on 2023-12-28 11:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_profile', '0002_alter_address_alternate_number_alter_address_name_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='address',
            name='alternate_number',
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
        migrations.AlterField(
            model_name='address',
            name='number',
            field=models.CharField(max_length=15),
        ),
    ]