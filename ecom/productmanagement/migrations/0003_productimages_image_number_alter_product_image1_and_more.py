# Generated by Django 5.0 on 2023-12-21 05:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('productmanagement', '0002_product_image1_productimages'),
    ]

    operations = [
        migrations.AddField(
            model_name='productimages',
            name='image_number',
            field=models.PositiveIntegerField(blank=True, default=1),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='product',
            name='image1',
            field=models.ImageField(blank=True, upload_to='media/images/'),
        ),
        migrations.AlterField(
            model_name='productimages',
            name='images',
            field=models.ImageField(upload_to='media/images/'),
        ),
    ]