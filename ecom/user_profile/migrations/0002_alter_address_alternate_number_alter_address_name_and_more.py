# Generated by Django 5.0 on 2023-12-28 08:44

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("user_profile", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="address",
            name="alternate_number",
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="address",
            name="name",
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name="address",
            name="number",
            field=models.IntegerField(),
        ),
    ]
