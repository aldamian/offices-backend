# Generated by Django 4.0.2 on 2022-03-17 19:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_remove_office_layout_desk_x_pos_px_desk_x_size_m_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='building',
            name='address',
            field=models.CharField(max_length=200, unique=True),
        ),
    ]
