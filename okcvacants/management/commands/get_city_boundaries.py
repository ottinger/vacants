from django.contrib.gis.gdal import DataSource
from django.contrib.gis.utils import LayerMapping

import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "vacants_project.settings")
import django
import geopandas
from django.core.management.base import BaseCommand
from shapely.geometry import mapping

django.setup()

import okcvacants.models

PROJECT_ROOT = os.path.abspath(os.path.dirname(__name__))


class Command(BaseCommand):
    help = "Parses city boundaries from SHP/DBF format files."

    def handle(self, *args, **options):
        gdf = get_and_transform_gdf()

        for i in range(0, len(gdf)):
            cur_row = gdf.loc[i]
            print(cur_row)
            print(cur_row['boundary'])

            boundary = mapping(cur_row['boundary'])
            c_c = okcvacants.models.City(name=cur_row['name'],
                                         boundary=boundary,
                                         is_enabled=False)
            c_c.save()

        for c in okcvacants.models.City.objects.all():
            # We set all to disabled by default except for OKC (since we only have data from City of OKC)
            if c.name == "Oklahoma City":
                c.is_enabled = True
                c.save()

def get_and_transform_gdf():
    shp_path = PROJECT_ROOT + "/misc_files/city_boundaries_shapefiles/city_boundaries.shp"
    gdf = geopandas.read_file(shp_path)

    gdf = gdf.to_crs(epsg=4326)

    gdf = gdf.rename(columns={
        'City_Name': 'name',
        'geometry': 'boundary'
    })
    return gdf
