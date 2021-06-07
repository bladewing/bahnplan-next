from django.test import TestCase

from core.models.vehicle_type import VehicleType
from core.models.workshop_category import WorkshopCategory


class TestVehicleType(TestCase):
    def setUp(self):
        WorkshopCategory.objects.create(category=5)

    def test_create_valid(self):
        VehicleType.objects.create(name='BR 182', vocal_name='Taurus',
                                   workshop_category=WorkshopCategory.objects.get(category=5), v_max=230,
                                   total_price=2200000, cost_per_km=9.87, cost_per_hour=209.37, multi_head_limit=2,
                                   cargo_tons_limit=2300)

    def test_to_string_name(self):
        vehicle = VehicleType.objects.create(name='BR 182', vocal_name='Taurus',
                                             workshop_category=WorkshopCategory.objects.get(category=5), v_max=230,
                                             total_price=2200000, cost_per_km=9.87, cost_per_hour=209.37,
                                             multi_head_limit=2, cargo_tons_limit=2300)
        self.assertEqual('BR 182 (Taurus)', vehicle.__str__())

    def test_to_string_no_name(self):
        vehicle = VehicleType.objects.create(name='BR 182', workshop_category=WorkshopCategory.objects.get(category=5),
                                             v_max=230, total_price=2200000, cost_per_km=9.87, cost_per_hour=209.37,
                                             multi_head_limit=2, cargo_tons_limit=2300)
        self.assertEqual('BR 182', vehicle.__str__())
