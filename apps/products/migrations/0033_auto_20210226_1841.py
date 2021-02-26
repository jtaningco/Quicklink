# Generated by Django 3.0.6 on 2021-02-26 18:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0032_auto_20210226_0153'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='days',
            field=models.IntegerField(default=0, null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='orders',
            field=models.CharField(blank=True, max_length=55, null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='stock',
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
    ]
