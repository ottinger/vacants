'''
get_geocode.py

Calls Mapbox geocoding API to obtain coordinates for each address.
'''

import os
import requests
import json

import django
from django.core.management.base import BaseCommand
from django.contrib.gis.geos import Point

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "vacants_project.settings")
django.setup()

import okcvacants.models

# get_geocode()
#
# Calls the Mapbox API and returns the lat/lon for a single address.
def get_geocode(address, api_key):
    api_address = "https://api.mapbox.com/geocoding/v5/mapbox.places/" + address + ".json?access_token=" + \
                  api_key + "&autocomplete=false&types=address"
    print(address)
    r = requests.get(api_address)
    request_json = json.loads(r.text)
    return request_json['features'][0]['center']


class Command(BaseCommand):
    help = "Calls Mapbox geocoding API to get the latitude/longitude for all addresses in Property table."

    def add_arguments(self, parser):
        parser.add_argument('-k', '--api_key', type=str, help='Mapbox API key (if not defined in settings)')

    def handle(self, *args, **options):
        if options['api_key']:
            api_key = options['api_key']
        elif os.getenv('MAPBOX_KEY'):
            api_key = os.getenv('MAPBOX_KEY')
        else:
            raise Exception("Mapbox API key not specified")

        for o in okcvacants.models.Property.objects.all():
            if (o.corrected_address):
                geocode = get_geocode(o.corrected_address, api_key)
            else:
                geocode = get_geocode(o.address, api_key)
            o.lat = geocode[1]
            o.lon = geocode[0]
            o.latlon = Point(geocode[0], geocode[1])
            o.save()
            print(geocode)
