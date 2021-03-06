# Generated by Django 3.1.3 on 2021-01-16 14:24

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('abbrev', models.CharField(max_length=127)),
                ('ownership', models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='LeasingMode',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=127)),
                ('vocal_name', models.CharField(max_length=255)),
                ('factor_yearly', models.DecimalField(decimal_places=10, max_digits=12)),
                ('factor_weekly', models.DecimalField(decimal_places=10, max_digits=12)),
            ],
        ),
        migrations.CreateModel(
            name='Plan',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to='')),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='core.company')),
            ],
        ),
        migrations.CreateModel(
            name='Route',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=127)),
                ('type', models.CharField(choices=[('CG', 'Cargo'), ('LO', 'Local'), ('IC', 'Intercity')], max_length=2)),
                ('revenue_per_week', models.DecimalField(decimal_places=2, max_digits=12)),
                ('operator', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.company')),
            ],
        ),
        migrations.CreateModel(
            name='Station',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Tender',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('route', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='core.route')),
            ],
        ),
        migrations.CreateModel(
            name='WorkshopCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('vocal_name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Workshop',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('categories', models.ManyToManyField(to='core.WorkshopCategory')),
                ('station', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='core.station')),
            ],
        ),
        migrations.CreateModel(
            name='VehicleType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=127)),
                ('vocal_name', models.CharField(max_length=255)),
                ('vmax', models.IntegerField()),
                ('total_price', models.DecimalField(decimal_places=2, max_digits=12)),
                ('cost_per_km', models.DecimalField(decimal_places=10, max_digits=12)),
                ('cost_per_hour', models.DecimalField(decimal_places=10, max_digits=12)),
                ('multi_head_limit', models.IntegerField()),
                ('cargo_tons_limit', models.IntegerField()),
                ('workshop_categorie', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='core.workshopcategory')),
            ],
        ),
        migrations.CreateModel(
            name='Vehicle',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('leasing_mode', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='core.leasingmode')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='core.company')),
                ('plan', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.plan')),
                ('type', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='core.vehicletype')),
            ],
        ),
        migrations.CreateModel(
            name='TransportRequirement',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('destination', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='destination_for', to='core.station')),
                ('orgin', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='origin_for', to='core.station')),
                ('tender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='requirements', to='core.tender')),
            ],
        ),
        migrations.CreateModel(
            name='TrackLimit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('station', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='core.station')),
                ('tender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.tender')),
            ],
        ),
        migrations.CreateModel(
            name='Track',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=255)),
                ('type', models.CharField(choices=[('CG', 'Cargo'), ('LO', 'Local'), ('IC', 'Intercity')], max_length=2)),
                ('length', models.DecimalField(decimal_places=6, max_digits=10)),
                ('price', models.DecimalField(decimal_places=2, max_digits=5)),
                ('tracks', models.IntegerField(max_length=3)),
                ('travel_time_in_minutes', models.IntegerField()),
                ('min_speed', models.IntegerField()),
                ('end', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='end_of', to='core.station')),
                ('start', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='start_of', to='core.station')),
                ('tender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.tender')),
            ],
        ),
        migrations.AddField(
            model_name='tender',
            name='workshops',
            field=models.ManyToManyField(to='core.Workshop'),
        ),
        migrations.AddField(
            model_name='plan',
            name='route',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='core.route'),
        ),
        migrations.AddField(
            model_name='plan',
            name='tender',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='core.tender'),
        ),
        migrations.CreateModel(
            name='Criterion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=127)),
                ('weight', models.DecimalField(decimal_places=10, max_digits=12)),
                ('tender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.tender')),
            ],
        ),
    ]
