# Generated by Django 3.0.6 on 2021-03-07 23:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0063_orderinformation'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderinformation',
            name='token_key',
            field=models.CharField(blank=True, max_length=999, null=True),
        ),
    ]