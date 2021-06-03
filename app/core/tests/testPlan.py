import shutil

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase

from core.models import Plan, Company, Tender, Route

TEST_ROUTE = 'KBS 100 Hamburg - Rostock'


class TestLeasingMode(TestCase):
    def setUp(self):
        Company.objects.create(name='Testbahn', abbrev='TB')
        self.mock_file = SimpleUploadedFile("test_file.xlsx", b"some content!")
        self.test_route = Route.objects.create(name=TEST_ROUTE, type=Route.LOCAL)
        self.test_tender = Tender.objects.create(route=Route.objects.get(name=TEST_ROUTE))

    def test_create_valid(self):
        Plan.objects.create(creator=Company.objects.get(name='Testbahn'), file=self.mock_file)
        Plan.objects.create(creator=Company.objects.get(name='Testbahn'), file=self.mock_file, tender=self.test_tender,
                            route=self.test_route)

    def test_is_active(self):
        inactive_plan = Plan.objects.create(creator=Company.objects.get(name='Testbahn'), file=self.mock_file)
        self.assertFalse(inactive_plan.is_active())
        active_plan = Plan.objects.create(creator=Company.objects.get(name='Testbahn'), file=self.mock_file,
                                          tender=self.test_tender, route=self.test_route)
        self.assertTrue(active_plan.is_active())

    def test_to_string(self):
        inactive_plan = Plan.objects.create(creator=Company.objects.get(name='Testbahn'), file=self.mock_file)
        self.assertEquals("1 (TB)", inactive_plan.__str__())
        active_plan = Plan.objects.create(creator=Company.objects.get(name='Testbahn'), file=self.mock_file,
                                          tender=self.test_tender, route=self.test_route)
        self.assertEquals("2 LO KBS 100 Hamburg - Rostock (TB)", active_plan.__str__())

    def tearDown(self):
        shutil.rmtree('plans/')
