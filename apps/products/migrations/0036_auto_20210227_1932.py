# Generated by Django 3.0.6 on 2021-02-27 11:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0035_product_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='orders',
            field=models.CharField(blank=True, default=0, max_length=55, null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='stock',
            field=models.CharField(blank=True, default=0, max_length=55, null=True),
        ),
    ]