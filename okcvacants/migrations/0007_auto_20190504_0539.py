# Generated by Django 2.2 on 2019-05-04 05:39

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('okcvacants', '0006_neighborhood_boundary_area'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='property',
            name='lat',
        ),
        migrations.RemoveField(
            model_name='property',
            name='lon',
        ),
    ]
