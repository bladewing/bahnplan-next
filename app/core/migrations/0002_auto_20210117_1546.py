# Generated by Django 3.1.3 on 2021-01-17 14:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vehicletype',
            name='cost_per_hour',
            field=models.DecimalField(decimal_places=6, max_digits=12),
        ),
        migrations.AlterField(
            model_name='vehicletype',
            name='cost_per_km',
            field=models.DecimalField(decimal_places=6, max_digits=12),
        ),
    ]
