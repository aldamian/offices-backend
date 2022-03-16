# Generated by Django 4.0.2 on 2022-03-16 16:12

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_rename_building_address_building_address'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='office',
            name='layout',
        ),
        migrations.AddField(
            model_name='desk',
            name='x_pos_px',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='desk',
            name='x_size_m',
            field=models.FloatField(default=0.0),
        ),
        migrations.AddField(
            model_name='desk',
            name='y_pos_px',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='desk',
            name='y_size_m',
            field=models.FloatField(default=0.0),
        ),
        migrations.AddField(
            model_name='office',
            name='desk_ids',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.PositiveIntegerField(), blank=True, null=True, size=None),
        ),
        migrations.AddField(
            model_name='office',
            name='x_size_m',
            field=models.FloatField(default=0.0),
        ),
        migrations.AddField(
            model_name='office',
            name='y_size_m',
            field=models.FloatField(default=0.0),
        ),
    ]