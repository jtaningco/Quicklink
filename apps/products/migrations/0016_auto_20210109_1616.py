# Generated by Django 3.0.6 on 2021-01-09 08:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0015_auto_20210108_2234'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='image_one',
            field=models.ImageField(null=True, upload_to='products'),
        ),
        migrations.AlterField(
            model_name='product',
            name='image_three',
            field=models.ImageField(blank=True, null=True, upload_to='products'),
        ),
        migrations.AlterField(
            model_name='product',
            name='image_two',
            field=models.ImageField(blank=True, null=True, upload_to='products'),
        ),
    ]
