# Import django modules
from django.conf.urls import patterns, include, url


urlpatterns = patterns('lakegis_app.views',
    url(r'^$', 'index', name='lakegis_app-index'),
)
