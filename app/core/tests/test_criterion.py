from django.test import TestCase

from core.models.criterion import Criterion
from core.models.route import Route
from core.models.station import Station
from core.models.tender import Tender
from core.models.workshop import Workshop

TEST_ROUTE = 'KBS 100 Hamburg - Rostock'


class TestCriterion(TestCase):

    def setUp(self):
        Route.objects.create(name=TEST_ROUTE, type=Route.LOCAL)
        Station.objects.create(name='Hagen Hbf')
        Workshop.objects.create(name='Bw Hagen', station=Station.objects.get(name="Hagen Hbf"))
        self.tender = Tender.objects.create(route=Route.objects.get(name=TEST_ROUTE))

    def test_crate_valid(self):
        Criterion.objects.create(tender=self.tender, name='Preis', weight=100.0)

    def test_to_string(self):
        criterion = Criterion.objects.create(tender=self.tender, name='Preis', weight=100.0)
        self.assertEqual('Preis', criterion.__str__())
