from django.test import TestCase

from core.models.line import Line
from core.models.route import Route
from core.models.tender import Tender

TEST_ROUTE = 'KBS 100 Hamburg - Rostock'


class TestLine(TestCase):
    def setUp(self):
        Route.objects.create(name=TEST_ROUTE, type=Route.LOCAL)
        self.tender = Tender.objects.create(route=Route.objects.get(name=TEST_ROUTE))

    def test_create_valid(self):
        Line.objects.create(tender=self.tender, name='RE Hamburg - Rostock')

    def test_to_string(self):
        line = Line.objects.create(tender=self.tender, name='RE Hamburg - Rostock')
        self.assertEqual('RE Hamburg - Rostock (KBS 100 Hamburg - Rostock)', line.__str__())
