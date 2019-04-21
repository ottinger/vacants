from django.shortcuts import render
from django.http import HttpResponse, Http404
from django.template import loader

from .models import Property

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
