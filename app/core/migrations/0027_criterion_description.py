# Generated by Django 3.2.5 on 2021-07-16 22:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0026_auto_20210716_2217'),
    ]

    operations = [
        migrations.AddField(
            model_name='criterion',
            name='description',
            field=models.CharField(max_length=511, null=True),
        ),
    ]