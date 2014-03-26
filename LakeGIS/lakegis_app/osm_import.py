# coding: utf-8
import os

import models

class RegionImportError(Exception):
    pass

class ShapefileArchiveError(RegionImportError):
    pass

class ShapefileError(RegionImportError):
    pass

def _extract_files(archive, destdir, files):
    for f in files:
        output_dir = os.path.join(destdir, os.path.dirname(f))
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        output_file = open(os.path.join(destdir, f), 'wb')
        output_file.write(archive.getmember(f).read())
        output_file.close()

def _download(url, destination):
    import urllib
    urllib.urlretrieve(url, destination)

def _feature_field_set(feature, field):
    return feature.get(field) != ''

def _polygon_to_multipolygon(wkt):
    if wkt[:4] == 'POLY':
        wkt = wkt.replace('POLYGON (', 'MULTIPOLYGON((') + ')'

    return wkt

def _line_to_multiline(wkt):
    if wkt[:4] == 'LINE':
        wkt = wkt.replace('LINESTRING (', 'MULTILINESTRING((') + ')'

    return wkt


def _add_water(feature, region):
    # Болота не добавляем
    if feature.get('NATURAL') == 'wetland':
        return

    name = None
    if not _feature_field_set(feature, 'NAME'):
        name = '[Безымянный водоем]'
    else:
        name = feature.get('NAME')

    wkt = feature.geom.wkt
    if feature.geom_type == 'Polygon':
        wkt = _polygon_to_multipolygon(wkt)

    water = models.WaterModel.objects.create(name = name, geom = wkt, region = region)
    water.save()

def _add_forest(feature, region):
    if feature.get('NATURAL') != 'forest' and feature.get('WOOD') == '':
        return

    name = None
    if not _feature_field_set(feature, 'NAME'):
        name = '[Безымянный лес]'
    else:
        name = feature.get('NAME')

    wkt = feature.geom.wkt
    if feature.geom_type == 'Polygon':
        wkt = _polygon_to_multipolygon(wkt)

    forest = models.ForestModel.objects.create(name = name, geom = wkt, region = region)
    forest.save()

def _add_settlement(feature, region):
    name = None
    if not _feature_field_set(feature, 'NAME'):
        name = '[Безымянный населенный пункт]'
    else:
        name = feature.get('NAME')

    wkt = feature.geom.wkt
    if feature.geom_type == 'Polygon':
        wkt = _polygon_to_multipolygon(wkt)

    settlement = models.SettlementModel.objects.create(name = name, geom = wkt, region = region)
    settlement.save()

def _add_highway(feature, region):
    proper_highway_classes = [
            'motorway',
            'trunk',
            'primary',
#            'secondary',
#            'tertiary'
    ]
    if not feature.get('HIGHWAY') in proper_highway_classes:
        return
    name = None
    if not _feature_field_set(feature, 'NAME'):
        name = feature.get('REF')
        if name == '':
            name = '[Безымянная трасса]'
    else:
        name = feature.get('NAME')

    wkt = feature.geom.wkt
    if feature.geom_type == 'Linestring':
        wkt = _line_to_multiline(wkt)

    highway = models.HighwayModel.objects.create(name = name, geom = wkt, region = region)
    highway.save()

def _add_railway_station(feature, region):
    proper_railway_stations = [
            'station',
            'halt'
    ]
    if not feature.get('RAILWAY') in proper_railway_stations:
        return
    
    name = None
    if not _feature_field_set(feature, 'NAME'):
        name = '[Безымянная станция]'
    else:
        name = feature.get('NAME')

    wkt = feature.geom.wkt
    station = models.RailwayStationModel.objects.create(name = name, geom = wkt, region = region)
    station.save()

def _import_layer(region, data_archive, data_dir, shapefile_basename, model, import_fun):
    from django.contrib.gis.gdal import DataSource

    SHAPEFILE_EXTENSIONS = ['.shp', '.dbf', '.shx']
    shapefiles = [shapefile_basename + extension for extension in SHAPEFILE_EXTENSIONS]
    _extract_files(data_archive, data_dir, shapefiles)
    main_shapefile = os.path.join(data_dir, shapefiles[0])
    data_source = DataSource(main_shapefile)
    model.objects.filter(region__exact = region).delete()
    layer = data_source[0]
    for feature in layer:
        import_fun(feature, region)

def import_region(region):
    import shutil
    import tempfile
    import py7zlib
    import django.contrib.gis.gdal.error
    
    tempdir = tempfile.mkdtemp()
    filename = os.path.join(tempdir, 'region.7z')
    
    try:
        _download(region.shapefile_archive_url, filename)
        archive_file = open(filename, 'rb')
        archive = py7zlib.Archive7z(archive_file)

        # Тут импортируются данные
        imported_layers = [
                ('data/water-polygon', models.WaterModel, _add_water),
                ('data/vegetation-polygon', models.ForestModel, _add_forest),
                ('data/settlement-polygon', models.SettlementModel, _add_settlement),
                ('data/highway-line', models.HighwayModel, _add_highway),
                ('data/railway-station-point', models.RailwayStationModel, _add_railway_station)
        ]
        for imported_layer in imported_layers:
            _import_layer(region, archive, tempdir, imported_layer[0], imported_layer[1], imported_layer[2])
    except py7zlib.ArchiveError as e:
        raise ShapefileArchiveError(str(e))
    except django.contrib.gis.gdal.error.OGRException as e:
        raise ShapefileError(str(e))
    except django.contrib.gis.geos.error.GEOSException as e:
        raise ShapefileError(str(e))
    finally:
        shutil.rmtree(tempdir)

