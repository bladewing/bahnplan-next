# Generated by Django 3.1.13 on 2021-10-30 12:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_auto_20210809_0045'),
    ]

    operations = [
        migrations.AddField(
            model_name='criterion',
            name='userinput',
            field=models.BooleanField(default=False),
        ),
        migrations.CreateModel(
            name='CriterionValue',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.DecimalField(decimal_places=5, max_digits=12)),
                ('criterion', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.criterion')),
            ],
        ),
        migrations.CreateModel(
            name='Application',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ulp', models.FilePathField(path='/var/tmp/ulp')),
                ('company', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.company')),
                ('criterions', models.ManyToManyField(to='core.CriterionValue')),
                ('tender', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.tender')),
            ],
            options={
                'verbose_name': 'Application',
                'verbose_name_plural': 's',
            },
        ),
    ]