# coding: utf-8
import models
import osm_import

def import_region(region):
    osm_import.import_region(region)
    # Тут будет код, запускающий импорт баз отдыха для соответствующего региона

def import_all_regions():
    for region in models.RegionModel.objects.all():
        import_region(region)
