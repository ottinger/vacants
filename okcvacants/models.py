from django.db import models

# Create your models here.
class Property(models.Model):
    # This will contain the fields in the Abandoned Buildings List for now.
    # May break the data down/add more fields later.
    case_number = models.CharField(max_length=20)
    address = models.CharField(max_length=150)
    declared_date = models.DateTimeField()
    ward_number = models.IntegerField()
    parcel_number = models.IntegerField()  # This is OKC's parcel number, not to be confused with County Assessor's!

    # lat/lon will be DecimalField for now. We may set up a proper GIS database later
    lat = models.DecimalField(max_digits=12, decimal_places=9, default=0)
    lon = models.DecimalField(max_digits=12, decimal_places=9, default=0)
