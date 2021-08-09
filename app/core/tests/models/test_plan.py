from unittest import mock

from django.core.files import File
from django.core.files.storage import Storage
from django.test import TestCase

from core.models.company import Company
from core.models.plan import Plan
from core.models.route import Route
from core.models.tender import Tender

TEST_ROUTE = 'KBS 100 Hamburg - Rostock'


class TestPlan(TestCase):
    TEST_FILE_NAME = 'test1.xlsx'

    def setUp(self):
        Company.objects.create(name='Testbahn', abbrev='TB')
        self.test_route = Route.objects.create(name=TEST_ROUTE, type=Route.LOCAL)
        self.test_tender = Tender.objects.create(route=Route.objects.get(name=TEST_ROUTE))

        # Mocking a file for testing that does not manipulate file system
        self.mock_file = mock.MagicMock(spec=File, name='FileMock')
        self.mock_file.name = self.TEST_FILE_NAME
        self.mock_file.__str__.return_value = self.TEST_FILE_NAME

        # Mock storage to avoid having to remove files after testing
        self.storage_mock = mock.MagicMock(spec=Storage, name='StorageMock')
        self.storage_mock.url = mock.MagicMock(name='url')
        self.storage_mock.url.return_value = 'plans/test1.jpg'

        # fix issues caused by mocked storage
        self.image_field_mock = mock.MagicMock(name='get_db_prep_save')
        self.image_field_mock.return_value = self.TEST_FILE_NAME

    def test_create_valid(self):
        with mock.patch('django.core.files.storage.default_storage._wrapped', self.storage_mock):
            with mock.patch('django.db.models.FileField.get_db_prep_save', self.image_field_mock):
                Plan.objects.create(creator=Company.objects.get(name='Testbahn'), file=self.mock_file)
                Plan.objects.create(creator=Company.objects.get(name='Testbahn'), file=self.mock_file,
                                    tender=self.test_tender, route=self.test_route)

    def test_is_active(self):
        with mock.patch('django.core.files.storage.default_storage._wrapped', self.storage_mock):
            with mock.patch('django.db.models.FileField.get_db_prep_save', self.image_field_mock):
                inactive_plan = Plan.objects.create(creator=Company.objects.get(name='Testbahn'), file=self.mock_file)
                self.assertFalse(inactive_plan.is_active())
                active_plan = Plan.objects.create(creator=Company.objects.get(name='Testbahn'), file=self.mock_file,
                                                  tender=self.test_tender, route=self.test_route)
                self.assertTrue(active_plan.is_active())

    def test_to_string(self):
        with mock.patch('django.core.files.storage.default_storage._wrapped', self.storage_mock):
            with mock.patch('django.db.models.FileField.get_db_prep_save', self.image_field_mock):
                inactive_plan = Plan.objects.create(creator=Company.objects.get(name='Testbahn'), file=self.mock_file)
                self.assertEquals("1 (TB)", inactive_plan.__str__())
                active_plan = Plan.objects.create(creator=Company.objects.get(name='Testbahn'), file=self.mock_file,
                                                  tender=self.test_tender, route=self.test_route)
                self.assertEquals("2 KBS 100 Hamburg - Rostock (TB)", active_plan.__str__())
