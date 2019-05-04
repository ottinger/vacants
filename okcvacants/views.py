from django.shortcuts import render
from django.http import HttpResponse, Http404
from django.template import loader

from django.core.serializers import serialize

from .models import Property
from .models import Neighborhood

# index()
#
# Displays a list of properties.
def index(request):
    property_list = Property.objects.order_by('declared_date')

    template = loader.get_template('list_view.html')
    context = {'property_list': property_list}
    return HttpResponse(template.render(context, request))


# individual_view()
#
# Displays details for an individual property (presently no map)
def individual_view(request, id=None):
    try:
        property = Property.objects.get(pk=id)
    except Property.DoesNotExist:
        raise Http404("Could not find property")
    context = {'p': property}
    return render(request, 'individual_view.html', context)


# map_view()
#
# Displays a map of all neighborhoods and properties.
def map_view(request, neighborhood=None, properties=None):
    if not neighborhood:
        neighborhood = Neighborhood.objects.all()
        properties = Property.objects.all()

    properties_geojson = serialize('geojson', properties,
                                   geometry_field='latlon',
                                   fields=('latlon', 'address', 'pk'))
    neighborhoods_geojson = serialize('geojson', neighborhood,
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
        neighborhood = Neighborhood.objects.get(pk=id)
    except Neighborhood.DoesNotExist:
        raise Http404("Could not find neighborhood")

    return map_view(
        request,
        neighborhood=[neighborhood],
        properties=[x for x in Property.objects.all() if neighborhood.boundary.contains(x.latlon)]
    )

# search_page()
#
# Renders a search page with the list of neighborhood names.
def neighborhood_search_page(request):
    neighborhood_list = Neighborhood.objects.order_by('name')
    return render(request, "search.html", {'neighborhood_list': neighborhood_list})

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
