# Generated by Django 4.0.2 on 2022-03-16 14:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='office',
            name='layout',
            field=models.TextField(blank=True),
        ),
    ]
