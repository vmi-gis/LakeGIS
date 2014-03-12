from django.contrib.gis.db import models

class WaterModel(models.Model):
    name = models.CharField(max_length = 50)
    geom = models.MultiPolygonField()

    objects = models.GeoManager()

    def __unicode__(self):
        return self.name

class ForestModel(models.Model):
    name = models.CharField(max_length = 50)
    geom = models.MultiPolygonField()

    objects = models.GeoManager()

    def __unicode__(self):
        return self.name

class SettlementModel(models.Model):
    name = models.CharField(max_length = 50)
    geom = models.MultiPolygonField()

    objects = models.GeoManager()

    def __unicode__(self):
        return self.name

class RecreationCenterModel(models.Model):
    name = models.CharField(max_length = 50)
    geom = models.MultiPolygonField()

    objects = models.GeoManager()

    def __unicode__(self):
        return self.name

class HighwayModel(models.Model):
    name = models.CharField(max_length = 50)
    geom = models.MultiLineStringField()

    objects = models.GeoManager()

    def __unicode__(self):
        return self.name

class RailwayModel(models.Model):
    name = models.CharField(max_length = 50)
    geom = models.MultiLineStringField()

    objects = models.GeoManager()

    def __unicode__(self):
        return self.name

