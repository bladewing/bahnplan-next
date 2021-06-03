from decimal import Decimal

from django.test import TestCase

from core.models import LeasingMode


class TestLeasingMode(TestCase):
    def test_create_valid(self):
        LeasingMode.objects.create(name='Leasing 3', factor_yearly=Decimal("10.0"), factor_weekly=Decimal("0.06"))

    def test_to_string(self):
        mode = LeasingMode.objects.create(name='Leasing 3', factor_yearly=Decimal("10.0"),
                                          factor_weekly=Decimal("0.06"))
        self.assertEqual('Leasing 3', mode.__str__())
