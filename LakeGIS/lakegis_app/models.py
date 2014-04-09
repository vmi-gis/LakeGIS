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


class RecreationCenterModel(models.Model):
    name = models.CharField(max_length = 200)
    geom = models.PointField()
    region = models.ForeignKey(RegionModel)

    objects = models.GeoManager()

    #The following fields contain all the nearest objects to recreation center (in kilometres)
    dist_to_water = models.FloatField()
    nearest_water = models.ForeignKey(WaterModel)

    dist_to_forest = models.FloatField()
    nearest_forest = models.ForeignKey(ForestModel)

    dist_to_highway = models.FloatField()
    nearest_highway = models.ForeignKey(HighwayModel)

    dist_to_railway_station = models.FloatField()
    nearest_railway_station = models.ForeignKey(RailwayStationModel)

    dist_to_settlement = models.FloatField()
    nearest_settlement = models.ForeignKey(SettlementModel)
    #----------------------------------------

    def __unicode__(self):
        return self.name + ' (' + self.region.name + ')'