# Generated by Django 3.0.6 on 2021-02-26 20:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0034_auto_20210226_2014'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='time',
            field=models.CharField(max_length=10, null=True),
        ),
    ]
