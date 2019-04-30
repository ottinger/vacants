from django.contrib.gis.gdal import DataSource
from django.contrib.gis.utils import LayerMapping

import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "vacants_project.settings")
import django
from django.core.management.base import BaseCommand

django.setup()

import okcvacants.models

PROJECT_ROOT = os.path.abspath(os.path.dirname(__name__))


class Command(BaseCommand):
    help = "Parses neighborhood boundaries from SHP/DBF format files, and creates Neighborhood objects."

    def handle(self, *args, **options):
        ds = DataSource(PROJECT_ROOT + "/okc_neighborhoods.dbf")

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
