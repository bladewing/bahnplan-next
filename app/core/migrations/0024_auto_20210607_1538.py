# Generated by Django 3.1.4 on 2021-06-07 13:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0023_auto_20210607_1254'),
    ]

    operations = [
        migrations.RenameField(
            model_name='transportrequirement',
            old_name='endtime',
            new_name='end_time',
        ),
        migrations.RenameField(
            model_name='transportrequirement',
            old_name='orgin',
            new_name='origin',
        ),
        migrations.RenameField(
            model_name='transportrequirement',
            old_name='starttime',
            new_name='start_time',
        ),
        migrations.RenameField(
            model_name='transportrequirement',
            old_name='ttype',
            new_name='type',
        ),
        migrations.AlterField(
            model_name='transportrequirement',
            name='frequency',
            field=models.CharField(choices=[('ONCE', 'once'), ('HOURLY', 'hourly'), ('DAILY', 'daily')], max_length=6),
        ),
    ]
