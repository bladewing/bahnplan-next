# Generated by Django 3.1.4 on 2021-04-25 19:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0012_auto_20210424_2254'),
    ]

    operations = [
        migrations.RenameField(
            model_name='route',
            old_name='ttype',
            new_name='type',
        ),
    ]
