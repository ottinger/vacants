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
        okcvacants.models.Neighborhood.objects.all().delete()  # clear the Neighborhood table

        ds = DataSource(PROJECT_ROOT + "/misc_files/neighborhoods_shapefiles/okc_neighborhoods.dbf")

        mapping = {'name': 'Associatio',
                   'type': 'Type',
                   'boundary': 'POLYGON'}

        lm = LayerMapping(okcvacants.models.Neighborhood, ds, mapping)
        lm.save(verbose=True)

        for n in okcvacants.models.Neighborhood.objects.all():
            # Calculate the area for each Neighborhood
            # note that EPSG 32124 apparently ends in northern Norman. if we go further south, this may be an issue
            n.boundary.transform(32124)
            n.boundary_area = (n.boundary.area / 2589988.11) * 640  # Acres
            n.save()

            # For Neighborhoods with very large area we'd like to hide in the map view, set
            # neighborhoods_map_enabled to False
            map_disabled_names = ["Downtown Oklahoma City Inc", "Friends of 10th Street", "MPHHE Security",
                                  "Mustard Seed Development Corporation", "Urban Neighbors NA",
                                  "Windsor Area"]
            if n.name in map_disabled_names:
                n.neighborhoods_map_enabled = False

            # Find Properties in each Neighborhood
            n.boundary.transform(4326)
            for p in okcvacants.models.Property.objects.all():
                if n.boundary.contains(p.latlon):
                    n.properties.add(p)
                    n.save()
                    print("property added for " + str(n))
