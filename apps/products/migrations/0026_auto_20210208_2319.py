# Generated by Django 3.0.6 on 2021-02-08 15:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0025_product_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
    ]
