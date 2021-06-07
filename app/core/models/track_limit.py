from django.db.models import Model, ForeignKey, CASCADE, PROTECT, IntegerField

from core.models.station import Station
from core.models.tender import Tender


class TrackLimit(Model):
    WAY_TO_STRING = "min Fahrzeit"
    DEFAULT_TIME_TO_REACH = 0
    DEFAULT_NUMBER = 2
    DEFAULT_MAX_USAGE = 120

    """The usage of a station by each tender can be limited with TrackLimit"""
    tender = ForeignKey(Tender, on_delete=CASCADE)
    station = ForeignKey(Station, on_delete=PROTECT, related_name='+')
    number = IntegerField(default=DEFAULT_NUMBER)
    max_usage_in_minutes = IntegerField(default=DEFAULT_MAX_USAGE)
    time_to_reach_in_minutes = IntegerField(default=DEFAULT_TIME_TO_REACH)

    def __str__(self):
        return f"{self.station.name} ({self.number}x {self.max_usage_in_minutes} min{self.time_to_reach_description()})"

    def time_to_reach_description(self):
        if self.time_to_reach_in_minutes == 0:
            return ""
        return f", {self.time_to_reach_in_minutes} {self.WAY_TO_STRING}"
