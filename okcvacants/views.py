from django.shortcuts import render
from django.http import HttpResponse, Http404
from django.template import loader
from django.core.paginator import Paginator

from djgeojson.serializers import Serializer as GeoJSONSerializer

import csv

from .models import Property
from .models import Neighborhood
from .models import City


# map_view()
#
# Displays a map of all neighborhoods and properties.
def map_view(request, neighborhood=None, properties=None):
    if not neighborhood:
        neighborhood = Neighborhood.objects.exclude(properties__isnull=True).exclude(neighborhoods_map_enabled=False)
        properties = Property.objects.all()

    properties_geojson = GeoJSONSerializer().serialize(properties, properties=['latlon', 'pk','address'],
                                                       geometry_field='latlon', use_natural_keys=True,
                                                       with_modelname=False)
    neighborhoods_geojson = GeoJSONSerializer().serialize(neighborhood,
                                                          properties=['name', 'pk', 'type', 'boundary',
                                                                      'boundary_area', 'property_count',
                                                                      'property_density'],
                                                          geometry_field='boundary', use_natural_keys=True,
                                                          with_modelname=False)

    cities = City.objects.exclude(is_enabled=False)
    cities_geojson = GeoJSONSerializer().serialize(cities, geometry_field='boundary', use_natural_keys=True, with_modelname=False)

    context = {'properties_geojson': properties_geojson,
               'neighborhoods_geojson': neighborhoods_geojson,
               'cities_geojson': cities_geojson}
    return render(request, "map_view.html", context)


# property_list_view()
#
# Displays a list of properties.
def property_list_view(request):
    property_list = Property.objects.order_by('declared_date')
    paginator = Paginator(property_list, 100)

    page = request.GET.get('page')
    context = {'property_list': paginator.get_page(page)}
    template = loader.get_template('property_list_view.html')
    return HttpResponse(template.render(context, request))


# property_view()
#
# Displays details for an individual property (presently no map)
def property_view(request, id=None):
    try:
        property = Property.objects.get(pk=id)
    except Property.DoesNotExist:
        raise Http404("Could not find property")
    property_geojson = property.latlon
    property_neighborhoods = []
    context = {'p': property,
               'property_geojson': property_geojson,
               'property_neighborhoods': property_neighborhoods}
    return render(request, 'property_individual_view.html', context)


# property_search_page()
#
# Has a search box with a list of property addresses.
def property_search_page(request):
    property_list = Property.objects.order_by('address')
    return render(request, "property_search.html", {'property_list': property_list})


# do_property_search()
#
# Takes the property address, and returns the property page view.
def do_property_search(request):
    # Find the property id
    property_address = request.GET.get("property_address")
    try:
        property = Property.objects.get(short_address=property_address)
    except Neighborhood.DoesNotExist:
        raise Http404("Could not find property")

    # Return result from neighborhood_view()
    return property_view(request, property.id)

# neighborhood_list_view()
#
# Show list of neighborhoods (no map)
def neighborhood_list_view(request):
    neighborhood_list = Neighborhood.objects.order_by('name')
    all_properties = Property.objects.all()

    for n in neighborhood_list:
        n.all_properties = n.properties.all()
        n.properties_count = len(n.all_properties)
        # calculate properties per acre
        n.properties_per_sq_mi = n.properties_count / (n.boundary_area / 640)

    paginator = Paginator(neighborhood_list, 100)
    page = request.GET.get('page')

    template = loader.get_template('neighborhood_list_view.html')
    return HttpResponse(template.render({'neighborhood_list': paginator.get_page(page)}, request))


# neighborhood_view()
#
# Given the neighborhood id, displays a map of the neighborhood along with properties in it.
def neighborhood_view(request, id=None):
    try:
        n = Neighborhood.objects.get(pk=id)
        n.all_properties = n.properties.all()
        n.properties_count = len(n.all_properties)
        n.properties_per_sq_mi = n.properties_count / (n.boundary_area / 640)
    except Neighborhood.DoesNotExist:
        raise Http404("Could not find neighborhood")

    props = [x for x in n.properties.all()]
    properties_geojson = GeoJSONSerializer().serialize(props,
                                                       properties=['latlon', 'address', 'pk'],
                                                       geometry_field='latlon',
                                                       use_natural_keys=True,
                                                       with_modelname=False)
    print(properties_geojson)
    neighborhoods_geojson = GeoJSONSerializer().serialize([n],
                                                          properties=['boundary', 'type', 'name', 'pk', 'boundary_area',
                                                                      'property_count', 'property_density'],
                                                          geometry_field='boundary',
                                                          use_natural_keys=True,
                                                          with_modelname=False)
    print(neighborhoods_geojson)
    context = {'n': n,
               'neighborhoods_geojson': neighborhoods_geojson,
               'properties_geojson': properties_geojson}
    return render(request, 'neighborhood_individual_view.html', context)


# neighborhood_search_page()
#
# Has a search box with a list of neighborhoods.
def neighborhood_search_page(request):
    neighborhood_list = Neighborhood.objects.order_by('name')
    return render(request, "neighborhood_search.html", {'neighborhood_list': neighborhood_list})

# do_neighborhood_search()
#
# Takes the name of a neighborhood, and returns a view from neighborhood_view(). Neighborhood name
# must be exact (autocomplete is provided in the search template).
def do_neighborhood_search(request):
    # Find the neighborhood id
    neighborhood_name = request.GET.get("neighborhood_name")
    try:
        neighborhood = Neighborhood.objects.get(name=neighborhood_name)
    except Neighborhood.DoesNotExist:
        raise Http404("Could not find neighborhood")

    # Return result from neighborhood_view()
    return neighborhood_view(request, neighborhood.id)


# export_csv()
#
# Returns a CSV file containing data on all properties.
def export_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="vacants.csv"'

    writer = csv.writer(response)
    writer.writerow(['case_number', 'address', 'declared_date', 'ward_number', 'parcel_number', 'lon', 'lat'])
    for p in Property.objects.all():
        writer.writerow([p.case_number, p.address, p.declared_date, p.ward_number, p.parcel_number,
                         p.latlon[0], p.latlon[1]])

    return response


# about_page()
#
# Displays the about page from ./templates/about.html
def about_page(request):
    return render(request, 'about.html')
