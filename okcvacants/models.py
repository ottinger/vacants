from django.db import models
from django.contrib.gis.db import models
from django.contrib.gis.geos import Point

# Create your models here.
class Property(models.Model):
    # This will contain the fields in the Abandoned Buildings List for now.
    # May break the data down/add more fields later.
    case_number = models.CharField(max_length=20)
    address = models.CharField(max_length=150)
    declared_date = models.DateTimeField()
    ward_number = models.IntegerField()
    parcel_number = models.IntegerField()  # This is OKC's parcel number, not to be confused with County Assessor's!

    latlon = models.PointField(default=Point(0, 0))

    # If the address is incorrectly formatted or the geocoder chokes on it, we'll manually set it here (while
    # keeping the original). For example, the geocoder thinks one of the addresses is near Kansas City.
    corrected_address = models.CharField(max_length=150, null=True)

class Neighborhood(models.Model):
    name = models.CharField(max_length=150)
    type = models.CharField(max_length=150)
    boundary = models.GeometryField()
    boundary_area = models.FloatField(null=True)  # value is in acres

    # There can be multiple Neighborhoods for each Property, and (of course) multiple Properties
    # for each Neighborhood.
    #
    # Example: Mesta Park HP is overlapped by MPHHE Security. Therefore, a Property in Mesta Park
    # will have a relationship with both Neighborhoods.
    properties = models.ManyToManyField(Property)

    # This is an option to enable/disable showing the neighborhood on the main map. Some of these organizations
    # overlap multiple neighborhoods and make it hard to find more granular neighborhoods. We'll disable these for
    # now; they can still be found on the list/search pages.
    #
    # Examples: Mustard Seed Development Corp, Urban Neighbors NA, Downtown OKC Inc, Friends of 10th Street,
    # MPHHE Security, Windsor Area
    neighborhoods_map_enabled = models.BooleanField(default=True)

    def __str__(self):
        return self.name + " (" + str(self.id) + ")"
