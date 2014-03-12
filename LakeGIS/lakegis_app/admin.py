from django.contrib.gis import admin
from django.db.models import get_models, get_app
from django.contrib.admin.sites import AlreadyRegistered
import lakegis_app

# Register your models here.
app_models = get_app('lakegis_app')
for model in get_models(app_models):
    try:
        admin.site.register(model, admin.OSMGeoAdmin)
    except AlreadyRegistered:
        pass

