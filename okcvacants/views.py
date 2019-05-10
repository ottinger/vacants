from django.shortcuts import render
from django.http import HttpResponse, Http404
from django.template import loader
from django.core.paginator import Paginator

from django.core.serializers import serialize

from .models import Property
from .models import Neighborhood

# index()
#
# Displays a list of properties.
def index(request):
    property_list = Property.objects.order_by('declared_date')
    paginator = Paginator(property_list, 100)

    page = request.GET.get('page')
    context = {'property_list': paginator.get_page(page)}
    template = loader.get_template('list_view.html')
    return HttpResponse(template.render(context, request))


# individual_view()
#
# Displays details for an individual property (presently no map)
def individual_view(request, id=None):
    try:
        property = Property.objects.get(pk=id)
    except Property.DoesNotExist:
        raise Http404("Could not find property")
    property_geojson = serialize('geojson', [property],
                                 geometry_field='latlon',
                                 fields=('latlon', 'address', 'pk'))
    context = {'p': property,
               'property_geojson': property_geojson}
    return render(request, 'individual_view.html', context)


# map_view()
#
# Displays a map of all neighborhoods and properties.
def map_view(request, neighborhood=None, properties=None):
    if not neighborhood:
        neighborhood = Neighborhood.objects.exclude(properties__isnull=True).exclude(neighborhoods_map_enabled=False)
        properties = Property.objects.all()

    properties_geojson = serialize('geojson', properties,
                                   geometry_field='latlon',
                                   fields=('latlon', 'address', 'pk'))
    neighborhoods_geojson = serialize('neighborhood_geojson', neighborhood,
                                      geometry_field='boundary',
                                      fields=('boundary', 'name', 'type', 'pk'))

    context = {'properties_geojson': properties_geojson,
               'neighborhoods_geojson': neighborhoods_geojson}
    return render(request, "map_view.html", context)


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

    template = loader.get_template('neighborhood_list_view.html')
    return HttpResponse(template.render({'neighborhood_list': neighborhood_list}, request))


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

    properties_geojson = serialize('geojson', [x for x in Property.objects.all() if n.boundary.contains(x.latlon)],
                                   geometry_field='latlon',
                                   fields=('latlon', 'address', 'pk'))
    print(properties_geojson)
    neighborhoods_geojson = serialize('neighborhood_geojson', [n],
                                      geometry_field='boundary',
                                      fields=('boundary', 'name', 'type', 'pk'))
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


# property_search_page()
#
# Has a search box with a list of property addresses.
def property_search_page(request):
    property_list = Property.objects.order_by('address')
    return render(request, "property_search.html", {'property_list': property_list})


# do_neighborhood_search()
#
# Takes the property address, and returns the property page view.
def do_property_search(request):
    # Find the property id
    property_address = request.GET.get("property_address")
    try:
        property = Property.objects.get(address=property_address)
    except Neighborhood.DoesNotExist:
        raise Http404("Could not find property")

    # Return result from neighborhood_view()
    return individual_view(request, property.id)
