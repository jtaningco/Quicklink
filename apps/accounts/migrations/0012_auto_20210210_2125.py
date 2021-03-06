# Generated by Django 3.0.6 on 2021-02-10 13:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0011_auto_20210210_2123'),
    ]

    operations = [
        migrations.AlterField(
            model_name='openhours',
            name='from_hour',
            field=models.PositiveSmallIntegerField(choices=[(1, '1:00 AM'), (2, '2:00 AM'), (3, '3:00 AM'), (4, '4:00 AM'), (5, '5:00 AM'), (6, '6:00 AM'), (7, '7:00 AM'), (8, '8:00 AM'), (9, '9:00 AM'), (10, '10:00 AM'), (11, '11:00 AM'), (12, '12:00 AM'), (13, '13:00 AM'), (14, '14:00 AM'), (15, '15:00 AM'), (16, '16:00 AM'), (17, '17:00 AM'), (18, '18:00 AM'), (19, '19:00 AM'), (20, '20:00 AM'), (21, '21:00 AM'), (22, '22:00 AM'), (23, '23:00 AM'), (24, '24:00 AM')], default=None, null=True),
        ),
        migrations.AlterField(
            model_name='openhours',
            name='to_hour',
            field=models.PositiveSmallIntegerField(choices=[(1, '1:00 AM'), (2, '2:00 AM'), (3, '3:00 AM'), (4, '4:00 AM'), (5, '5:00 AM'), (6, '6:00 AM'), (7, '7:00 AM'), (8, '8:00 AM'), (9, '9:00 AM'), (10, '10:00 AM'), (11, '11:00 AM'), (12, '12:00 AM'), (13, '13:00 AM'), (14, '14:00 AM'), (15, '15:00 AM'), (16, '16:00 AM'), (17, '17:00 AM'), (18, '18:00 AM'), (19, '19:00 AM'), (20, '20:00 AM'), (21, '21:00 AM'), (22, '22:00 AM'), (23, '23:00 AM'), (24, '24:00 AM')], default=None, null=True),
        ),
    ]
