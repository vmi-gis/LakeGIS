# coding: utf8
from django.test import TestCase
import os
from lakegis_app import models
from lakegis_app import data_import
from lakegis_app import osm_import

class DataImportCase(TestCase):
    def setUp(self):
        test_data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'test_data')
        models.RegionModel.objects.create(name = u'Cutted', shapefile_archive_url = u'file://' + os.path.join(test_data_dir, 'cutted.7z'))
        models.RegionModel.objects.create(name = u'Corrupted shapefile', shapefile_archive_url = u'file://' + os.path.join(test_data_dir, 'corrupted_shapefile.7z'))
        models.RegionModel.objects.create(name = u'Corrupted archive', shapefile_archive_url = u'file://' + os.path.join(test_data_dir, 'corrupted_archive.7z'))
        models.RegionModel.objects.create(name = u'Nonexistent archive', shapefile_archive_url = u'http://example.com/nonexistant.7z')
    def test_normal_import(self):
        cutted_region = models.RegionModel.objects.get(name = u'Cutted')
        data_import.import_region(cutted_region)

        for model in [models.WaterModel, models.ForestModel, models.SettlementModel, models.HighwayModel, models.RailwayStationModel]:
            self.assertTrue(model.objects.count() > 0)

    def test_corrupted_shapefile(self):
        corrupted_shapefile_region = models.RegionModel.objects.get(name = u'Corrupted shapefile')
        try:
            data_import.import_region(corrupted_shapefile_region)
        except osm_import.ShapefileError:
            got_exception = True
        else:
            got_exception = False

        self.assertTrue(got_exception)

    def test_corrupted_archive(self):
        corrupted_archive_region = models.RegionModel.objects.get(name = u'Corrupted archive')
        try:
            data_import.import_region(corrupted_archive_region)
        except osm_import.ShapefileArchiveError:
            got_exception = True
        else:
            got_exception = False

        self.assertTrue(got_exception)

    def test_nonexistent_archive(self):
        nonexistent_archive_region = models.RegionModel.objects.get(name = u'Nonexistent archive')
        try:
            data_import.import_region(nonexistent_archive_region)
        except osm_import.ShapefileArchiveError:
            got_exception = True
        else:
            got_exception = False

        self.assertTrue(got_exception)

