from django.contrib.gis.db import models

class RegionModel(models.Model):
    name = models.CharField(max_length = 50)
    shapefile_archive_url = models.URLField()

    def __unicode__(self):
        return self.name

class RegionBorderModel(models.Model):
    geom = models.MultiPolygonField()
    region = models.ForeignKey(RegionModel)

    objects = models.GeoManager()

    def __unicode__(self):
        return self.region.name

class WaterModel(models.Model):
    name = models.CharField(max_length = 50)
    geom = models.MultiPolygonField()
    region = models.ForeignKey(RegionModel)

    objects = models.GeoManager()

    def __unicode__(self):
        return self.name + ' (' + self.region.name + ')'

class ForestModel(models.Model):
    name = models.CharField(max_length = 50)
    geom = models.MultiPolygonField()
    region = models.ForeignKey(RegionModel)

    objects = models.GeoManager()

    def __unicode__(self):
        return self.name + ' (' + self.region.name + ')'

class SettlementModel(models.Model):
    name = models.CharField(max_length = 50)
    geom = models.MultiPolygonField()
    region = models.ForeignKey(RegionModel)

    objects = models.GeoManager()

    def __unicode__(self):
        return self.name + ' (' + self.region.name + ')'

class RecreationCenterModel(models.Model):
    name = models.CharField(max_length = 50)
    geom = models.PointField()
    region = models.ForeignKey(RegionModel)

    objects = models.GeoManager()

    def __unicode__(self):
        return self.name + ' (' + self.region.name + ')'

class HighwayModel(models.Model):
    name = models.CharField(max_length = 50)
    geom = models.MultiLineStringField()
    region = models.ForeignKey(RegionModel)

    objects = models.GeoManager()

    def __unicode__(self):
        return self.name + ' (' + self.region.name + ')'

class RailwayStationModel(models.Model):
    name = models.CharField(max_length = 50)
    geom = models.PointField()
    region = models.ForeignKey(RegionModel)

    objects = models.GeoManager()

    def __unicode__(self):
        return self.name + ' (' + self.region.name + ')'

