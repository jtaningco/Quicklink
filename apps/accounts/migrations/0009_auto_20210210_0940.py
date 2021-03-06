# Generated by Django 3.0.6 on 2021-02-10 09:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0008_auto_20210210_0939'),
    ]

    operations = [
        migrations.CreateModel(
            name='OpenHours',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('day_from', models.PositiveSmallIntegerField(choices=[(1, 'Monday'), (2, 'Tuesday'), (3, 'Wednesday'), (4, 'Thursday'), (5, 'Friday'), (6, 'Saturday'), (7, 'Sunday')], unique=True)),
                ('day_to', models.PositiveSmallIntegerField(choices=[(1, 'Monday'), (2, 'Tuesday'), (3, 'Wednesday'), (4, 'Thursday'), (5, 'Friday'), (6, 'Saturday'), (7, 'Sunday')])),
                ('from_hour', models.PositiveSmallIntegerField(choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8), (9, 9), (10, 10), (11, 11), (12, 12), (13, 13), (14, 14), (15, 15), (16, 16), (17, 17), (18, 18), (19, 19), (20, 20), (21, 21), (22, 22), (23, 23), (24, 24)])),
                ('to_hour', models.PositiveSmallIntegerField(choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8), (9, 9), (10, 10), (11, 11), (12, 12), (13, 13), (14, 14), (15, 15), (16, 16), (17, 17), (18, 18), (19, 19), (20, 20), (21, 21), (22, 22), (23, 23), (24, 24)])),
            ],
        ),
        migrations.RemoveField(
            model_name='shopinformation',
            name='shop_days_open',
        ),
        migrations.AlterField(
            model_name='shoplogo',
            name='logo',
            field=models.ImageField(blank=True, null=True, upload_to='logos'),
        ),
        migrations.DeleteModel(
            name='Days',
        ),
        migrations.AddField(
            model_name='shopinformation',
            name='shop_delivery_schedule',
            field=models.ManyToManyField(to='accounts.OpenHours'),
        ),
    ]
