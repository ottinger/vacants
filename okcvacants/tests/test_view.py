from django.urls import reverse
from django.test import TestCase

from okcvacants.models import Property
import datetime
from django.contrib.gis.geos import Point


class PropertyViewTestCase(TestCase):
    def setUp(self):
        self.p = Property()

        self.p.case_number = "C01-23456"
        self.p.address = "2501 W MEMORIAL RD OKLAHOMA CITY, OK 73134"
        self.p.short_address = "2501 W MEMORIAL RD"
        self.p.declared_date = datetime.datetime.strptime("01/01/2019", "%m/%d/%Y").date()
        self.p.ward_number = 8
        self.p.parcel_number = 12345
        self.p.latlon = Point(35.613333, -97.558333)

        self.p.save()

    def test_property_view(self):
        response = self.client.get(reverse('property', kwargs={'id': self.p.id}))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "C01-23456")  # case number
        self.assertContains(response, "2501 W MEMORIAL RD OKLAHOMA CITY, OK 73134")  # full address
        self.assertContains(response, "01/01/2019")  # declared date
        self.assertContains(response, "12345")  # parcel number
        self.assertContains(response, "[35.613333, -97.558333]")  # coordinates (in javascript)

    def test_property_list_view(self):
        response = self.client.get(reverse('properties'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "C01-23456")  # case number
        self.assertContains(response, "2501 W MEMORIAL RD")  # short or long address is ok
        self.assertContains(response, "01/01/2019")  # declared date
        self.assertContains(response, reverse('property', kwargs={'id': self.p.id}))  # url to individual view

    def test_map_view(self):
        response = self.client.get(reverse('map'))

        self.assertContains(response, "2501 W MEMORIAL RD")  # short or long address is ok
        self.assertContains(response, "[35.613333, -97.558333]")  # coordinates (in javascript)
