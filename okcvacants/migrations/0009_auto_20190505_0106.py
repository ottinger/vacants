# Generated by Django 2.2 on 2019-05-05 01:06

import django.contrib.gis.db.models.fields
import django.contrib.gis.geos.point
from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('okcvacants', '0008_neighborhood_properties'),
    ]

    operations = [
        migrations.AlterField(
            model_name='neighborhood',
            name='boundary',
            field=django.contrib.gis.db.models.fields.GeometryField(srid=4326),
        ),
        migrations.AlterField(
            model_name='property',
            name='latlon',
            field=django.contrib.gis.db.models.fields.PointField(default=django.contrib.gis.geos.point.Point(0, 0),
                                                                 srid=4326),
        ),
    ]
