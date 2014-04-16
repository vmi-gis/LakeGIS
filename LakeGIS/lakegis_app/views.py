from django.shortcuts import render_to_response 
from django.http import HttpResponse


# Import custom modules

def index(request):
    'Display map'
    return render_to_response('lakegis_app/index.html')
    
# Create your views here.
