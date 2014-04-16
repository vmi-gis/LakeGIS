# Import django modules
from django.conf.urls import patterns, include, url
from lakegis_app.rest import GetAllRecreationCenters, FilterRecreationCenters

urlpatterns = patterns('lakegis_app.views',
    url(r'^$', 'index', name='lakegis_app-index'),
    url(r'^all_rcs/$', GetAllRecreationCenters.as_view()),
    url(r'^filter_rcs/$', FilterRecreationCenters.as_view())
)
