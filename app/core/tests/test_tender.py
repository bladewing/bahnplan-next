from datetime import timedelta

from django.test import TestCase
from django.utils.timezone import now

from core.models.route import Route
from core.models.station import Station
from core.models.tender import Tender
from core.models.workshop import Workshop

TEST_WORKSHOP = 'Bw Hagen'
TEST_ROUTE = 'KBS 100 Hamburg - Rostock'
TEST_DESCRIPTION = """Die Stadt Hamburg, die Nahverkehrsgesellschaft Schleswig-Holstein und das Verkehrsministerium 
    Mecklenburg-Vorpommern schreiben aus."""


class TenderModelTest(TestCase):

    def setUp(self):
        Route.objects.create(name=TEST_ROUTE, type=Route.LOCAL)
        Station.objects.create(name='Hagen Hbf')
        Workshop.objects.create(name='Bw Hagen', station=Station.objects.get(name="Hagen Hbf"))

    @staticmethod
    def test_create_valid_min():
        Tender.objects.create(route=Route.objects.get(name=TEST_ROUTE))

    @staticmethod
    def test_create_valid_full():
        Tender.objects.create(route=Route.objects.get(name=TEST_ROUTE), text=TEST_DESCRIPTION, start_date=now(),
                              end_date=now() + timedelta(days=2 * 365))

    @staticmethod
    def test_add_workshop():
        tender = Tender.objects.create(route=Route.objects.get(name=TEST_ROUTE))
        tender.workshops.add(Workshop.objects.get(name=TEST_WORKSHOP))

    def test_to_string(self):
        tender = Tender.objects.create(route=Route.objects.get(name=TEST_ROUTE), text=TEST_DESCRIPTION,
                                       start_date=now(), end_date=now() + timedelta(days=2 * 365))
        self.assertEquals(tender.__str__(), TEST_ROUTE)
