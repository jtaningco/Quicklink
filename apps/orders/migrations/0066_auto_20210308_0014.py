# Generated by Django 3.0.6 on 2021-03-08 00:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0065_auto_20210308_0007'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderinformation',
            name='token_jwt_id',
            field=models.CharField(blank=True, max_length=999, null=True),
        ),
        migrations.AlterField(
            model_name='orderinformation',
            name='token_id',
            field=models.CharField(blank=True, max_length=55, null=True),
        ),
    ]