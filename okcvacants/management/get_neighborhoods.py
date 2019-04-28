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

# Calculate the area for each Neighborhood
for o in okcvacants.models.Neighborhood.objects.all():
    # note that EPSG 32124 apparently ends in northern Norman. if we go further south, this may be an issue
    o.boundary.transform(32124)  # TODO: check if transform is saved?
    o.boundary_area = (o.boundary.area / 2589988.11) * 640  # Acres
    o.save()

    pass
