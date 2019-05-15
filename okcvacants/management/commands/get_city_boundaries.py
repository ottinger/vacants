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
    help = "Parses city boundaries from SHP/DBF format files."

    def handle(self, *args, **options):
        ds = DataSource(PROJECT_ROOT + "/misc_files/city_boundaries_shapefiles/city_boundaries.dbf")

        mapping = {'name': 'City_Name',
                   'boundary': 'POLYGON'}

        lm = LayerMapping(okcvacants.models.City, ds, mapping)
        lm.save(verbose=True)

        for c in okcvacants.models.City.objects.all():
            # We set all to disabled by default except for OKC (since we only have data from City of OKC)
            if c.name == "Oklahoma City":
                c.is_enabled = True
                c.save()
