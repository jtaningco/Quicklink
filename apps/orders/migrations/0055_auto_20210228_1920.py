# Generated by Django 3.0.6 on 2021-02-28 11:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0038_auto_20210228_1700'),
        ('orders', '0054_auto_20210228_1700'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productorder',
            name='addons',
            field=models.ManyToManyField(to='products.Addon'),
        ),
    ]