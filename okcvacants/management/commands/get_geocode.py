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
import vacants_project.tokens


# get_geocode()
#
# Calls the Mapbox API and returns the lat/lon for a single address.
def get_geocode(address):
    api_address = "https://api.mapbox.com/geocoding/v5/mapbox.places/" + address + ".json?access_token=" + \
                  vacants_project.tokens.MAPBOX_TOKEN + "&autocomplete=false&types=address"
    print(address)
    r = requests.get(api_address)
    request_json = json.loads(r.text)
    return request_json['features'][0]['center']


class Command(BaseCommand):
    help = "Calls Mapbox geocoding API to get the latitude/longitude for all addresses in Property table."

    def handle(self, *args, **options):
        for o in okcvacants.models.Property.objects.all():
            geocode = get_geocode(o.address)
            o.lat = geocode[1]
            o.lon = geocode[0]
            o.latlon = Point(geocode[0], geocode[1])
            o.save()
            print(geocode)
