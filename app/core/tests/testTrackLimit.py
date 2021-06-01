from django.test import TestCase

from core.models import *

TEST_STATION_NAME = 'Hagen Hbf'

TEST_WORKSHOP_NAME = 'Bw Hagen'
TEST_ROUTE = 'KBS 100 Hamburg - Rostock'
TEST_DESCRIPTION = """Die Stadt Hamburg, die Nahverkehrsgesellschaft Schleswig-Holstein und das Verkehrsministerium 
    Mecklenburg-Vorpommern schreiben aus."""


class TestTrackLimit(TestCase):
    def setUp(self):
        Route.objects.create(name=TEST_ROUTE, type=Route.LOCAL)
        Station.objects.create(name=TEST_STATION_NAME)
        Workshop.objects.create(name=TEST_WORKSHOP_NAME, station=Station.objects.get(name=TEST_STATION_NAME))
        Tender.objects.create(route=Route.objects.get(name=TEST_ROUTE))

    def test_create_valid_min(self):
        TrackLimit.objects.create(tender=Tender.objects.get(route=Route.objects.get(name=TEST_ROUTE)),
                                  station=Station.objects.get(name=TEST_STATION_NAME))

    def test_create_valid_full(self):
        TrackLimit.objects.create(tender=Tender.objects.get(route=Route.objects.get(name=TEST_ROUTE)),
                                  station=Station.objects.get(name=TEST_STATION_NAME), number=5,
                                  max_usage_in_minutes=18, time_to_reach_in_minutes=3)

    def test_to_string_min(self):
        self.test_create_valid_min()
        limit = TrackLimit.objects.get(station=Station.objects.get(name=TEST_STATION_NAME))
        self.assertEqual(limit.__str__(),
                         TEST_STATION_NAME + " (" + str(TrackLimit.DEFAULT_NUMBER) + "x " + str(
                             TrackLimit.DEFAULT_MAX_USAGE) + " min)")

    def test_to_string_full(self):
        self.test_create_valid_full()
        limit = TrackLimit.objects.get(station=Station.objects.get(name=TEST_STATION_NAME))
        self.assertEqual(limit.__str__(),
                         TEST_STATION_NAME + " (" + str(5) + "x " + str(
                             18) + " min, " + str(3) + " " + TrackLimit.WAY_TO_STRING + ")")
