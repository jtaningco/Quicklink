# Generated by Django 3.0.6 on 2021-01-05 09:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0002_auto_20210105_1648'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='notes',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
