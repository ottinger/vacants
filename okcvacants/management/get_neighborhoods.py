from django.contrib.gis.gdal import DataSource
from django.contrib.gis.utils import LayerMapping

import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "vacants_project.settings")
import django

django.setup()

import okcvacants.models

ds = DataSource("../../okc_neighborhoods.dbf")

mapping = {'name': 'Associatio',
           'type': 'Type',
           'boundary': 'POLYGON'}

lm = LayerMapping(okcvacants.models.Neighborhood, ds, mapping)
lm.save(verbose=True)
