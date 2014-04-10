# coding: utf8
import json
import math
import string
import urllib2

from django.conf import settings
from django.contrib.gis.geos import GEOSGeometry

import data_import_errors
import models


class HTTPCallError(data_import_errors.RegionImportError):
    pass


class MalformedServerResponse(data_import_errors.RegionImportError):
    pass


def _do_search(search_url):
    try:
        f = urllib2.urlopen(search_url)
        response_as_json = json.loads(f.read())
    except urllib2.URLError as e:
            raise HTTPCallError(str(e))
    except ValueError as e:
            raise MalformedServerResponse(str(e))
    return response_as_json


def _get_geom_envelope_max_span(geom):
    envelope = geom.ogr.envelope
    x_span = envelope.max_x - envelope.min_x
    y_span = envelope.max_y - envelope.min_y
    return max(x_span, y_span)


def _get_search_radius_for_geom(geom):
    NORTH_POLE_LAEA_RUSSIA_SRID = 3576
    geom_tr = geom.transform(NORTH_POLE_LAEA_RUSSIA_SRID, True)
    max_span = _get_geom_envelope_max_span(geom_tr)
    radius = int(math.ceil(max_span / math.sqrt(2)))
    return radius


def _get_returned_places(response):
    try:
        places = response['places']
    except KeyError:
        raise MalformedServerResponse('No places returned')
    return places


def _get_place_name(place):
    try:
        name = place['title']
    except KeyError:
        name = '[Неизвестно]'
    return name


def _get_place_tags(place):
    try:
        raw_tags = place['tags']
    except KeyError:
        tags = []
    else:
        tags = [raw_tag['id'] for raw_tag in raw_tags]
    return tags


def _get_place_wkt(place):
    try:
        lat = place['location']['lat']
        lon = place['location']['lon']
    except KeyError:
        raise MalformedServerResponse('o location information returned')
    return 'POINT({} {})'.format(lon, lat)


def _place_is_allowed(place, allowed_tags, forbidden_tags):
    tags = _get_place_tags(place)
    is_allowed = False
    for tag in tags:
        if tag in allowed_tags:
            is_allowed = True
        elif tag in forbidden_tags:
            is_allowed = False
            break
    return is_allowed


def _place_to_recreation_center(place, region):
    MAX_NAME_LENGTH = models.RecreationCenterModel._meta.get_field('name').max_length
    name = _get_place_name(place)[:MAX_NAME_LENGTH]
    geom = _get_place_wkt(place)
    return models.RecreationCenterModel(region = region, name = name, geom = geom)


def _recreation_center_exists(rc):
    return models.RecreationCenterModel.objects.filter(geom__exact = rc.geom).count() > 0


def _place_is_inside_geom(place, geom):
    return geom.contains(GEOSGeometry(_get_place_wkt(place)))


def _dist_to_water(rc):
    pnt = rc.geom
    wms_distance = []
    wms_geom = []
    for wm in models.WaterModel.objects.distance(pnt):
         wms_distance.append(wm.distance.km),
         wms_geom.append(wm.geom)
    rc.dist_to_water = min(wms_distance)
    w_index = wms_distance.index(min(wms_distance))
    rc.nearest_water = models.WaterModel.objects.get(geom__contains=wms_geom[w_index])


def _dist_to_forest(rc):
    pnt = rc.geom
    fs_distance = []
    fs_geom = []
    for f in models.ForestModel.objects.distance(pnt):
         fs_distance.append(f.distance.km),
         fs_geom.append(f.geom)
    rc.dist_to_forest = min(fs_distance)
    f_index = fs_distance.index(min(fs_distance))
    rc.nearest_forest = models.ForestModel.objects.get(geom__contains=fs_geom[f_index])


def _dist_to_highway(rc):
    pnt = rc.geom
    hws_distance = []
    hws_geom = []
    for hw in models.HighwayModel.objects.distance(pnt):
         hws_distance.append(hw.distance.km),
         hws_geom.append(hw.geom)
    rc.dist_to_highway = min(hws_distance)
    hw_index = hws_distance.index(min(hws_distance))
    rc.nearest_highway = models.HighwayModel.objects.get(geom__contains=hws_geom[hw_index])


def _dist_to_railway_station(rc):
    pnt = rc.geom
    rws_distance = []
    rws_geom = []
    for s in models.RailwayStationModel.objects.distance(pnt):
         rws_distance.append(s.distance.km),
         rws_geom.append(s.geom)
    rc.dist_to_railway_station = min(rws_distance)
    r_index = rws_distance.index(min(rws_distance))
    rc.nearest_railway_station = models.RailwayStationModel.objects.get(geom__contains=rws_geom[r_index])


def _dist_to_settlement(rc):
    pnt = rc.geom
    ss_distance = []
    ss_geom = []
    for sm in models.SettlementModel.objects.distance(pnt):
         ss_distance.append(sm.distance.km),
         ss_geom.append(sm.geom)
    rc.dist_to_settlement = min(ss_distance)
    sm_index = ss_distance.index(min(ss_distance))
    rc.nearest_settlement = models.SettlementModel.objects.get(geom__contains=ss_geom[sm_index])


def _process_response(server_response, region, region_border, allowed_tags, forbidden_tags):
    places = _get_returned_places(server_response)
    num_places = len(places)
    for place in places:
        if _place_is_allowed(place, allowed_tags, forbidden_tags) and _place_is_inside_geom(place, region_border.geom):
            recreation_center = _place_to_recreation_center(place, region)
            if not _recreation_center_exists(recreation_center):
                _dist_to_water(recreation_center),
                _dist_to_forest(recreation_center),
                _dist_to_highway(recreation_center),
                _dist_to_railway_station(recreation_center),
                _dist_to_settlement(recreation_center),
                recreation_center.save()

    return num_places


def _import_region(region, api_key, search_settings):
    SEARCH_URL_TEMPLATE = string.Template('http://api.wikimapia.org/?function=place.search&key=$api_key&q=$query_string&format=json&language=ru&page=$page&categories_or=$allowed_categories&data_blocks=main,location&lon=$lon&lat=$lat&distance=$distance&count=$count')
    MAX_RESULTS_PER_PAGE = 100

    border = models.RegionBorderModel.objects.get(region__exact = region)
    center_lon, center_lat = border.geom.centroid.coords
    search_radius = _get_search_radius_for_geom(border.geom)
    
    allowed_categories_as_str = ','.join(str(category) for category in search_settings['allowed_categories'])
    query_string = search_settings['query_string']
    
    search_url = string.Template(SEARCH_URL_TEMPLATE.safe_substitute(
            api_key = api_key, 
            query_string = query_string, 
            allowed_categories = allowed_categories_as_str, 
            lon = center_lon, 
            lat = center_lat, 
            distance = search_radius, 
            count = MAX_RESULTS_PER_PAGE
    ))
    page = 1
    places_returned = True
    while places_returned:
        response = _do_search(search_url.substitute(page = page))
        places_returned = _process_response(response, region, border, search_settings['allowed_categories'], search_settings['forbidden_categories'])
        page = page + 1



def import_region(region):
    api_key = settings.WIKIMAPIA_API_KEY
    if api_key == '':
        api_key = 'example'

    search_settings = settings.WIKIMAPIA_SEARCH_SETTINGS
    models.RecreationCenterModel.objects.filter(region__exact = region).delete()

    _import_region(region, api_key, search_settings)
