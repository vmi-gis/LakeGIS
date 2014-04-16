# coding: utf8

from rest_framework import serializers
from lakegis_app import models

class WaterSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.WaterModel
        fields = ['name', 'lat', 'lon']
    lat = serializers.FloatField(source = 'geom.centroid.y')
    lon = serializers.FloatField(source = 'geom.centroid.x')

class ForestSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ForestModel
        fields = ['name', 'lat', 'lon']
    lat = serializers.FloatField(source = 'geom.centroid.y')
    lon = serializers.FloatField(source = 'geom.centroid.x')

class SettlementSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.SettlementModel
        fields = ['name', 'lat', 'lon']
    lat = serializers.FloatField(source = 'geom.centroid.y')
    lon = serializers.FloatField(source = 'geom.centroid.x')

class HighwaySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.HighwayModel
        fields = ['name', 'lat', 'lon']
    lat = serializers.FloatField(source = 'geom.centroid.y')
    lon = serializers.FloatField(source = 'geom.centroid.x')


class RailwayStationSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.RailwayStationModel
        fields = ['name', 'lat', 'lon']
    lat = serializers.FloatField(source = 'geom.y')
    lon = serializers.FloatField(source = 'geom.x')

class RecreationCenterSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.RecreationCenterModel
        fields = [
                'id', 'name', 'lat', 'lon', 
                'dist_to_water', 'nearest_water',
                'dist_to_forest', 'nearest_forest',
                'dist_to_highway', 'nearest_highway',
                'dist_to_railway_station', 'nearest_railway_station',
                'dist_to_settlement', 'nearest_settlement'
        ]
    lat = serializers.FloatField(source = 'geom.y')
    lon = serializers.FloatField(source = 'geom.x')

    nearest_water = WaterSerializer()
    nearest_forest = ForestSerializer()
    nearest_highway = HighwaySerializer()
    nearest_railway_station = RailwayStationSerializer()
    nearest_settlement = SettlementSerializer()

