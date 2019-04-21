'''
get_geocode.py

Calls Mapbox geocoding API to obtain coordinates for each address.
'''

import os
import requests
import json

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "vacants_project.settings")
import django

django.setup()

import okcvacants.models


def get_geocode(address):
    api_address = "https://api.mapbox.com/geocoding/v5/mapbox.places/" + address + ".json?access_token=pk.eyJ1IjoibWF0dGZpY2tlIiwiYSI6ImNqNnM2YmFoNzAwcTMzM214NTB1NHdwbnoifQ.Or19S7KmYPHW8YjRz82v6g&autocomplete=false&types=address"
    print(address)
    r = requests.get(api_address)
    request_json = json.loads(r.text)
    return request_json['features'][0]['center']


for o in okcvacants.models.Property.objects.all():
    geocode = get_geocode(o.address)
    print(geocode)
