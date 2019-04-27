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


def serialized(request):
    x = serialize('geojson', Property.objects.all(),
                  geometry_field='latlon',
                  fields=('latlon', 'address'))
    print(x)
    return HttpResponse(x, content_type='application/json')
