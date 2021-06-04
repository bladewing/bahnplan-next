from datetime import date
from decimal import Decimal

from django.test import TestCase

from core.models import WorkshopCategory, Company
from core.models.leasing_mode import LeasingMode
from core.models.vehicle import Vehicle
from core.models.vehicle_type import VehicleType


class TestVehicle(TestCase):
    def setUp(self):
        self.leasing_3 = LeasingMode.objects.create(name='Leasing 3', factor_yearly=Decimal("10.0"),
                                                    factor_weekly=Decimal("0.06"))
        WorkshopCategory.objects.create(category=5)
        self.taurus = VehicleType.objects.create(name='182', vocal_name='Taurus',
                                                 workshop_category=WorkshopCategory.objects.get(category=5), v_max=230,
                                                 total_price=2200000, cost_per_km=9.87, cost_per_hour=209.37,
                                                 multi_head_limit=2, cargo_tons_limit=2300)
        self.company = Company.objects.create(name="Testbahn", abbrev="TB")

    def test_create_valid(self):
        Vehicle.objects.create(type=self.taurus, leasing_mode=self.leasing_3, owner=self.company,
                               leased_since=date.today())

    def test_to_string(self):
        vehicle = Vehicle.objects.create(type=self.taurus, leasing_mode=self.leasing_3, owner=self.company,
                                         leased_since=date.today())
        self.assertEquals("182-001", vehicle.__str__())
