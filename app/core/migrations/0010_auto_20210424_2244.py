# Generated by Django 3.1.4 on 2021-04-24 20:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0009_auto_20210424_2211'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='abbrev',
            field=models.CharField(max_length=8, unique=True),
        ),
    ]
