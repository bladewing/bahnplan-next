from django.test import TestCase

from core.models.station import Station
from core.models.workshop import Workshop
from core.models.workshop_category import WorkshopCategory


class WorkshopModelTest(TestCase):
    def setUp(self):
        Station.objects.create(name='Hagen Hbf')
        WorkshopCategory.objects.create(category=3)
        WorkshopCategory.objects.create(category=5)

    @staticmethod
    def test_create_valid():
        Workshop.objects.create(name='Bw Hagen', station=Station.objects.get(name="Hagen Hbf"))

    @staticmethod
    def test_add_categories():
        workshop = Workshop.objects.create(name='Bw Hagen', station=Station.objects.get(name="Hagen Hbf"))
        workshop.categories.add(WorkshopCategory.objects.get(category=5))
        workshop.categories.add(WorkshopCategory.objects.get(category=3))

    def test_to_string(self):
        workshop = Workshop.objects.create(name='Bw Hagen', station=Station.objects.get(name="Hagen Hbf"))
        workshop.categories.add(WorkshopCategory.objects.get(category=5))
        workshop.categories.add(WorkshopCategory.objects.get(category=3))
        self.assertEquals(workshop.__str__(), 'Bw Hagen in Hagen Hbf (Kategorie 3, 5)')
