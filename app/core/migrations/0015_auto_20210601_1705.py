# Generated by Django 3.1.4 on 2021-06-01 15:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0014_auto_20210525_2214'),
    ]

    operations = [
        migrations.RenameField(
            model_name='vehicletype',
            old_name='vmax',
            new_name='v_max',
        ),
        migrations.RenameField(
            model_name='vehicletype',
            old_name='workshop_categorie',
            new_name='workshop_category',
        ),
        migrations.AlterField(
            model_name='tracklimit',
            name='max_usage_in_minutes',
            field=models.IntegerField(default=120),
        ),
        migrations.AlterField(
            model_name='tracklimit',
            name='time_to_reach_in_minutes',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='vehicletype',
            name='name',
            field=models.CharField(max_length=127, unique=True),
        ),
        migrations.AlterField(
            model_name='vehicletype',
            name='vocal_name',
            field=models.CharField(blank=True, max_length=255),
        ),
    ]
