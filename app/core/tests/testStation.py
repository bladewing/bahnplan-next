from django.test import TestCase

from core.models import Station


class RouteModelTest(TestCase):
    TEST_STATION_NAME = 'Hamm (Westf.) Hbf'

    def test_create_valid(self):
        Station(name=self.TEST_STATION_NAME)

    def test_to_string(self):
        station = Station(name=self.TEST_STATION_NAME)
        self.assertEquals(station.__str__(), self.TEST_STATION_NAME)
