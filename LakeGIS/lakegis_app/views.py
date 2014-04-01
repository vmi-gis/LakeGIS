from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.template.loader import render_to_string
# Import custom modules
from lakegis_app.models import RecreationCenterModel

def index(request):
    'Display map'
    RecreationCenters = RecreationCenterModel.objects.order_by('name')
    return render_to_response('lakegis_app/index.html', {
        'lakegis_app': RecreationCenters,
        'content': render_to_string('lakegis_app/RecreationCenters.html', {'lakegis_app': RecreationCenters}),
    })
    
# Create your views here.
