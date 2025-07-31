import os

import geopandas
import django
from django.core.management.base import BaseCommand
from shapely import Point
from shapely.geometry import mapping, shape

import okcvacants.models

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "vacants_project.settings")

django.setup()

PROJECT_ROOT = os.path.abspath(os.path.dirname(__name__))


class Command(BaseCommand):
    help = "Parses neighborhood boundaries from SHP/DBF format files, and creates Neighborhood objects."

    def handle(self, *args, **options):
        okcvacants.models.Neighborhood.objects.all().delete()  # clear the Neighborhood table

        gdf = get_and_transform_gdf()
        print(gdf)

        for i in range(0, len(gdf)):
            cur_row = gdf.loc[i]
            print(cur_row['boundary'])

            boundary = mapping(cur_row['boundary'])
            c_n = okcvacants.models.Neighborhood(name=cur_row['name'],
                                                 type=cur_row['type'],
                                                 # boundary=cur_row['boundary'])
                                                 boundary=boundary,
                                                 boundary_area=cur_row['gdf_area'])
            c_n.save()

        for n in okcvacants.models.Neighborhood.objects.all():
            # For Neighborhoods with very large area we'd like to hide in the map view, set
            # neighborhoods_map_enabled to False
            map_disabled_names = ["Downtown Oklahoma City Inc", "Friends of 10th Street", "MPHHE Security",
                                  "Mustard Seed Development Corporation", "Urban Neighbors NA",
                                  "Windsor Area", "Envision 240"]
            if n.name in map_disabled_names:
                n.neighborhoods_map_enabled = False

            # Find Properties in each Neighborhood
            for p in okcvacants.models.Property.objects.all():
                if p.latlon:
                    p_point = Point(p.latlon['coordinates'])
                else:
                    continue

                boundary_poly = shape(n.boundary)
                if boundary_poly.contains(p_point):
                    n.properties.add(p)
                    n.save()
                    print("property added for " + str(n))


def get_and_transform_gdf():
    shp_path = PROJECT_ROOT + "/misc_files/neighborhoods_shapefiles/okc_neighborhoods.shp"
    gdf = geopandas.read_file(shp_path)

    # Calculate the area for each Neighborhood
    # note that EPSG 32124 apparently ends in northern Norman. if we go further south, this may be an issue
    gdf = gdf.to_crs(epsg=32124)
    gdf['gdf_area'] = gdf.geometry.area
    gdf['gdf_area'] = (gdf['gdf_area'] / 2589988.11) * 640  # Acres

    gdf = gdf.to_crs(epsg=4326)

    gdf = gdf.rename(columns={
        'Associatio': 'name',
        'Type': 'type',
        'geometry': 'boundary'
    })
    return gdf