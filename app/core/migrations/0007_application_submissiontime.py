# Generated by Django 3.1.14 on 2022-07-13 21:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_auto_20220608_2312'),
    ]

    operations = [
        migrations.AddField(
            model_name='application',
            name='submissiontime',
            field=models.DateTimeField(default=0),
            preserve_default=False,
        ),
    ]
