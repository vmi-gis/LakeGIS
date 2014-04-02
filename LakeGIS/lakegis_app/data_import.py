# coding: utf-8
import models
import osm_import
import wm_import

def import_region(region):
    osm_import.import_region(region)
    wm_import.import_region(region)

def import_all_regions():
    for region in models.RegionModel.objects.all():
        import_region(region)
