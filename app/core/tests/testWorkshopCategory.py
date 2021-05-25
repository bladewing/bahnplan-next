from django.test import TestCase

from core.models import WorkshopCategory


class WorkshopCategoryModelTest(TestCase):

    @staticmethod
    def test_create_valid():
        WorkshopCategory(category=5)

    def test_to_string(self):
        self.assertEquals(WorkshopCategory(category=5).__str__(), 'Kategorie 5')
