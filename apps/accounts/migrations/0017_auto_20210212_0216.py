# Generated by Django 3.0.6 on 2021-02-11 18:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0016_auto_20210212_0210'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Notifications',
            new_name='Notification',
        ),
        migrations.RenameModel(
            old_name='SocialMediaLinks',
            new_name='SocialMediaLink',
        ),
    ]
