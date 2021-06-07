import datetime

from django.db.models import *

from core.models.line import Line
from core.models.station import Station


class TransportRequirement(Model):
    """Demand which have to be transported to send a valid tender application."""
    ONCE = "ONCE"
    HOURLY = "HOURLY"
    DAILY = "DAILY"
    FREQUENCY_CHOICES = ((ONCE, 'once'), (HOURLY, 'hourly'), (DAILY, 'daily'),)
    frequency = CharField(max_length=6, choices=FREQUENCY_CHOICES)

    PASSENGERS = "PAS"
    CARGO = "CGO"
    TYPE_CHOICES = ((PASSENGERS, 'PAS'), (CARGO, 'CGO'),)
    type = CharField(max_length=3, choices=TYPE_CHOICES)

    line = ForeignKey(Line, on_delete=CASCADE)
    demand = IntegerField()
    origin = ForeignKey(Station, related_name='origin_for', on_delete=PROTECT)
    destination = ForeignKey(Station, related_name='destination_for', on_delete=PROTECT)
    start_time = TimeField(default=datetime.time(0, 0))
    end_time = TimeField(default=datetime.time(23, 59))
    mon = BooleanField()
    tue = BooleanField()
    wed = BooleanField()
    thu = BooleanField()
    fri = BooleanField()
    sat = BooleanField()
    sun = BooleanField()

    def __str__(self):
        days = f"{xo(self.mon)}{xo(self.tue)}{xo(self.wed)}{xo(self.thu)}{xo(self.fri)}|{xo(self.sat)}{xo(self.sun)}"

        return f"{self.line.tender.id}: {self.line.name} {days} {self.start_time:%H:%M} - {self.end_time:%H:%M} " \
               f"{self.frequency} {self.origin.name} -> {self.destination.name} ({self.demand} {self.type})"


def xo(day):
    if day:
        return 'X'
    return '0'
