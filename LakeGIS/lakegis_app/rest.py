from django.contrib.gis.measure import D
from lakegis_app.models import RecreationCenterModel, SettlementModel
from lakegis_app.serializers import RecreationCenterSerializer, SettlementSerializer
from rest_framework.generics import ListAPIView
from rest_framework.renderers import UnicodeJSONRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

class GetAllRecreationCenters(ListAPIView):
    renderer_classes = [UnicodeJSONRenderer]
    serializer_class = RecreationCenterSerializer

    def get_queryset(self):
        return RecreationCenterModel.objects.order_by('name')

class GetAllSettlements(ListAPIView):
    renderer_classes = [UnicodeJSONRenderer]
    serializer_class = SettlementSerializer

    def get_queryset(self):
        return SettlementModel.objects.order_by('name')

class FilterRecreationCenters(APIView):
    renderer_classes = [UnicodeJSONRenderer]

    def _valid_distance(self, value):
        try:
            float(value)
        except ValueError:
            return False
        else:
            return True

    def get(self, request):
        rcs = RecreationCenterModel.objects.all()
        params = request.GET

        if 'water_min' in params and self._valid_distance(params['water_min']):
            rcs = rcs.filter(dist_to_water__gte = float(params['water_min']))
        if 'water_max' in params and self._valid_distance(params['water_max']):
            rcs = rcs.filter(dist_to_water__lte = float(params['water_max']))

        if 'forest_min' in params and self._valid_distance(params['forest_min']):
            rcs = rcs.filter(dist_to_forest__gte = float(params['forest_min']))
        if 'forest_max' in params and self._valid_distance(params['forest_max']):
            rcs = rcs.filter(dist_to_forest__lte = float(params['forest_max']))

        if 'settlement_min' in params and self._valid_distance(params['settlement_min']):
            rcs = rcs.filter(dist_to_settlement__gte = float(params['settlement_min']))
        if 'settlement_max' in params and self._valid_distance(params['settlement_max']):
            rcs = rcs.filter(dist_to_settlement__lte = float(params['settlement_max']))

        if 'railway_station_min' in params and self._valid_distance(params['railway_station_min']):
            rcs = rcs.filter(dist_to_railway_station__gte = float(params['railway_station_min']))
        if 'railway_station_max' in params and self._valid_distance(params['railway_station_max']):
            rcs = rcs.filter(dist_to_railway_station__lte = float(params['railway_station_max']))

        if 'highway_min' in params and self._valid_distance(params['highway_min']):
            rcs = rcs.filter(dist_to_highway__gte = float(params['highway_min']))
        if 'highway_max' in params and self._valid_distance(params['highway_max']):
            rcs = rcs.filter(dist_to_highway__lte = float(params['highway_max']))

        spec_settlement_geom = SettlementModel.objects.get(id = params['spec_settlement_id']).geom
        if 'spec_settlement_min' in params and self._valid_distance(params['spec_settlement_min']):
            rcs = rcs.filter(geom__distance_gte = (spec_settlement_geom, D(km=float(params['spec_settlement_min']))))
        if 'spec_settlement_max' in params and self._valid_distance(params['spec_settlement_max']):
            rcs = rcs.filter(geom__distance_lte = (spec_settlement_geom, D(km=float(params['spec_settlement_max']))))

        serializer = RecreationCenterSerializer(rcs, many = True)
        return Response(serializer.data)
