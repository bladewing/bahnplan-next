from datetime import timedelta

from django.test import TestCase
# Create your tests here.
from django.utils.timezone import now

from core.models import Company, Route
from core.tests.utils import login_user


class RouteModelTest(TestCase):
    DEMO_ROUTE_NAME = 'KBS 100 Hamburg - Rostock'

    def test_create_valid(self):
        Route(operator=Company.create_owned_company(name="Testbahn", abbrev="TB", owners=login_user(self)),
              name=self.DEMO_ROUTE_NAME, type=Route.LONG_DISTANCE, revenue_per_week=5000.00, start_date=now(),
              end_date=now() + timedelta(days=2 * 365))

    def test_to_string(self):
        route = Route(operator=Company.create_owned_company(name="Testbahn", abbrev="TB", owners=login_user(self)),
                      name=self.DEMO_ROUTE_NAME, type=Route.LONG_DISTANCE, revenue_per_week=5000.00,
                      start_date=now(),
                      end_date=now() + timedelta(days=2 * 365))
        self.assertEquals(route.__str__(), 'IC KBS 100 Hamburg - Rostock (Testbahn)')
