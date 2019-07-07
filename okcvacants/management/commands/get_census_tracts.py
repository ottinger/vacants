import os
import requests
import json

import django
from django.core.management.base import BaseCommand
from django.contrib.gis.geos import GEOSGeometry

import okcvacants.models
from okcvacants.models import CensusTract

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "vacants_project.settings")
django.setup()


def get_geoid(address):
    census_url = "https://geocoding.geo.census.gov/geocoder/geographies/onelineaddress?benchmark=Public_AR_Current&vintage=Current_Current&address=" + address + "&format=json"

    r = requests.get(census_url)
    request_json = json.loads(r.text)
    if 'result' in request_json:
        if 'addressMatches' in request_json['result']:
            try:
                return request_json['result']['addressMatches'][0]['geographies']['Census Tracts'][0]['GEOID']
            except:
                return None


class Command(BaseCommand):
    help = "Calls US Census Bureau APIs to find census tract information for all properties."

    def add_arguments(self, parser):
        parser.add_argument('-k', '--api_key', type=str, help='US Census API key (if not defined in settings)')

    def handle(self, *args, **options):
        if options['api_key']:
            api_key = options['api_key']
        elif os.getenv('CENSUS_KEY'):
            api_key = os.getenv('CENSUS_KEY')
        else:
            raise Exception("US Census API key not specified")

    for o in okcvacants.models.Property.objects.all():
        if not o.census_tract:
            census_geoid = get_geoid(o.corrected_address if o.corrected_address else o.address)
            if census_geoid:
                print(o.address + " " + census_geoid)
                try:
                    tract = CensusTract.objects.get(geoid=census_geoid)
                except:
                    # Create CensusTract if necessary
                    tract = CensusTract()
                    tract.geoid = census_geoid

                    # Get the geojson containing polygon boundaries/etc from Census Bureau
                    r = requests.get(
                        "https://tigerweb.geo.census.gov/arcgis/rest/services/TIGERweb/tigerWMS_Current/MapServer/8/query?where=GEOID+%3D+" + census_geoid + "&text=&objectIds=&time=&geometry=&geometryType=esriGeometryEnvelope&inSR=&spatialRel=esriSpatialRelIntersects&relationParam=&outFields=*&returnGeometry=true&returnTrueCurves=false&maxAllowableOffset=&geometryPrecision=&outSR=&returnIdsOnly=false&returnCountOnly=false&orderByFields=&groupByFieldsForStatistics=&outStatistics=&returnZ=false&returnM=false&gdbVersion=&returnDistinctValues=false&resultOffset=&resultRecordCount=&queryByDistance=&returnExtentsOnly=false&datumTransformation=&parameterValues=&rangeValues=&f=geojson")
                    request_json = json.loads(r.text)
                    tract.name = request_json['features'][0]['properties']['NAME']
                    tract.county = request_json['features'][0]['properties']['COUNTY']

                    # Pull the feature from the geojson we got and create a geometry object
                    tract.boundary = GEOSGeometry(json.dumps(request_json['features'][0]['geometry']))
                    tract.save()

                o.CensusTract = tract
                o.save()

            else:
                print(o.address + " failed")
        else:
            print("tract already found: " + o.address)
