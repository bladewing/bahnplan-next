from django.test import TestCase

from core.models import Route, Tender, Station
from core.models.track import Track

MIN_SPEED = 160
TRAVEL_TIME_IN_MINUTES = 80
TRACKS = 2
PRICE = 507.878
LENGTH = 103.456
TEST_ROUTE = 'KBS 100 Hamburg - Rostock'


class TestTrack(TestCase):

    def setUp(self):
        Route.objects.create(name=TEST_ROUTE, type=Route.LOCAL)
        self.tender = Tender.objects.create(route=Route.objects.get(name=TEST_ROUTE))
        self.start = Station.objects.create(name='Hamburg Hbf')
        self.end = Station.objects.create(name='Hamburg Bergedorf')

    def test_create_valid(self):
        self.create_test_track()

    def create_test_track(self):
        return Track.objects.create(tender=self.tender, start=self.start, end=self.end, type=Route.LOCAL, length=LENGTH,
                                    price=PRICE, tracks=TRACKS, travel_time_in_minutes=TRAVEL_TIME_IN_MINUTES,
                                    min_speed=MIN_SPEED)

    def test_to_string(self):
        track = self.create_test_track()
        self.assertEqual('1 Hamburg Hbf -> Hamburg Bergedorf', track.__str__())

    def test_reverse_dependencies(self):
        track = self.create_test_track()
        self.assertTrue(track in self.start.start_of.all())
        self.assertTrue(track in self.end.end_of.all())
