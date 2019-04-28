from django.shortcuts import render
from django.http import HttpResponse, Http404
from django.template import loader

from django.core.serializers import serialize

from .models import Property
from .models import Neighborhood

# Create your views here.
def index(request):
    property_list = Property.objects.order_by('declared_date')
    '''
    response = ""
    for p in property_list:
        response += p.case_number + ": " + p.address + ", declared " + str(p.declared_date) + "<br>"
    return HttpResponse(response)
        '''
    template = loader.get_template('list_view.html')
    context = {'property_list': property_list}
    return HttpResponse(template.render(context, request))


def individual_view(request, id):
    try:
        property = Property.objects.get(pk=id)
    except Property.DoesNotExist:
        raise Http404("Could not find property")
    context = {'p': property}
    return render(request, 'individual_view.html', context)


def map_view(request):
    property_list = Property.objects.order_by('declared_date')
    template = loader.get_template('map_view.html')

    properties_geojson = serialize('geojson', Property.objects.all(),
                                   geometry_field='latlon',
                                   fields=('latlon', 'address'))
    print(properties_geojson)

    neighborhoods_geojson = serialize('geojson', Neighborhood.objects.all(),
                                      geometry_field='boundary',
                                      fields=('boundary', 'name', 'type'))

    context = {'property_list': property_list,
               'properties_geojson': properties_geojson,
               'neighborhoods_geojson': neighborhoods_geojson}
    return HttpResponse(template.render(context, request))


# neighborhood_list_view()
#
# Show list of neighborhoods (no map)
def neighborhood_list_view(request):
    neighborhood_list = Neighborhood.objects.order_by('name')
    all_properties = Property.objects.all()

    for x in all_properties:
        x.latlon.transform(32124)
    for n in neighborhood_list:
        # note that EPSG 32124 apparently ends in northern Norman. if we go further south, this may be an issue
        n.boundary.transform(32124)
        n.acres = (n.boundary.area / 2589988.11) * 640

        properties = [x for x in all_properties if n.boundary.contains(x.latlon)]
        n.properties_count = len(properties)

        n.properties_per_acre = n.properties_count / n.acres

    template = loader.get_template('neighborhood_list_view.html')
    return HttpResponse(template.render({'neighborhood_list': neighborhood_list}, request))


def neighborhood_view(request, id):
    try:
        neighborhood = Neighborhood.objects.get(pk=id)
    except Neighborhood.DoesNotExist:
        raise Http404("Could not find neighborhood")

    properties_geojson = serialize('geojson',
                                   [x for x in Property.objects.all() if neighborhood.boundary.contains(x.latlon)],
                                   geometry_field='latlon',
                                   fields=('latlon', 'address'))

    n_geojson = serialize('geojson', [neighborhood],
                          geometry_field='boundary',
                          fields={'boundary', 'name', 'type'})
    context = {'neighborhoods_geojson': n_geojson,
               'properties_geojson': properties_geojson}
    return render(request, 'map_view.html', context)


def serialized(request):
    x = serialize('geojson', Property.objects.all(),
                  geometry_field='latlon',
                  fields=('latlon', 'address'))
    print(x)
    return HttpResponse(x, content_type='application/json')
