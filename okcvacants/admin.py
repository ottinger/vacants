from django.contrib import admin
from .models import Property
from .models import Neighborhood
from .models import City

# Register your models here.
admin.site.register(Property)
admin.site.register(Neighborhood)
admin.site.register(City)
