from django.test import TestCase

from core.models.line import Line
from core.models.route import Route
from core.models.station import Station
from core.models.tender import Tender
from core.models.transport_requirement import TransportRequirement

TEST_ROUTE = 'KBS 100 Hamburg - Rostock'


class TestTransportRequirement(TestCase):
    def setUp(self):
        Route.objects.create(name=TEST_ROUTE, type=Route.LOCAL)
        self.tender = Tender.objects.create(route=Route.objects.get(name=TEST_ROUTE))
        self.line = Line.objects.create(tender=self.tender, name='RE Hamburg - Rostock')
        self.origin = Station.objects.create(name='Hamburg Hbf')
        self.destination = Station.objects.create(name='Hamburg Bergedorf')

    def test_create_valid(self):
        self.create_test_transport_requirement()

    def test_to_string(self):
        requirement = self.create_test_transport_requirement()
        self.assertEqual(
            '1: RE Hamburg - Rostock XXXXX|00 00:00 - 23:59 DAILY Hamburg Hbf -> Hamburg Bergedorf (2000 CGO)',
            requirement.__str__())

    def create_test_transport_requirement(self):
        return TransportRequirement.objects.create(line=self.line, type=TransportRequirement.CARGO,
                                                   frequency=TransportRequirement.DAILY, demand=2000,
                                                   origin=self.origin, destination=self.destination, mon=True, tue=True,
                                                   wed=True, thu=True, fri=True, sat=False, sun=False)
