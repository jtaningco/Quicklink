# Generated by Django 3.1.7 on 2021-03-31 06:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0044_auto_20210331_0632'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='description',
            field=models.CharField(max_length=140, null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='instructions',
            field=models.CharField(blank=True, default='', max_length=140, null=True),
        ),
    ]