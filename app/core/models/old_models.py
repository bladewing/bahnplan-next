from django.db.models import *

from core.models.station import Station
from core.models.tender import Tender


class Line(Model):
    """Lines are mostly like 'containers' holding different demands for tenders."""
    tender = ForeignKey(Tender, on_delete=CASCADE)
    name = CharField(max_length=127)

    def __str__(self):
        return self.name + " " + self.tender.__str__()


class TransportRequirement(Model):
    """Demand which have to be transported to send a valid tender application. Frequency, starttime and endtime should be in minutes, for the two later ones starting from midnight"""
    ONCE = "ONCE"
    HOURLY = "HRLY"
    DAILY = "DALY"
    FREQUENCY_CHOICES = ((ONCE, 'once'), (HOURLY, 'hourly'), (DAILY, 'daily'),)
    PASSENGERS = "PAS"
    CARGO = "CGO"
    TYPE_CHOICES = ((PASSENGERS, 'PAS'), (CARGO, 'CGO'),)
    line = ForeignKey(Line, on_delete=CASCADE)
    ttype = CharField(max_length=3, choices=TYPE_CHOICES)
    demand = IntegerField()
    frequency = CharField(max_length=4, choices=FREQUENCY_CHOICES)
    orgin = ForeignKey(Station, related_name='origin_for', on_delete=PROTECT)
    destination = ForeignKey(Station, related_name='destination_for', on_delete=PROTECT)
    starttime = IntegerField()
    endtime = IntegerField()
    mon = BooleanField()
    tue = BooleanField()
    wed = BooleanField()
    thu = BooleanField()
    fri = BooleanField()
    sat = BooleanField()
    sun = BooleanField()

    def __str__(self):
        days = "".join([("X" if self.mon else "O"), ("X" if self.tue else "O"), ("X" if self.wed else "O"),
                        ("X" if self.thu else "O"), ("X" if self.fri else "O"), "|", ("X" if self.sat else "O"),
                        ("X" if self.sun else "O"), ])
        return str(self.line.tender.id) + ": " + self.line.name + " " + days + " " + str(self.starttime) + "-" + str(
            self.endtime) + " " + str(
            self.frequency) + " " + self.orgin.name + "->" + self.destination.name + "(" + str(
            self.demand) + " " + self.ttype + ")"
