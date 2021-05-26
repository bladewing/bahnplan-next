from django.db.models import *

from core.models.company import Company
from core.models.route import Route
from core.models.station import Station
from core.models.tender import Tender
from core.models.workshop_category import WorkshopCategory


class TrackLimit(Model):
    """The usage of a station by each tender can be limited with TrackLimit"""
    tender = ForeignKey(Tender, on_delete=CASCADE)
    station = ForeignKey(Station, on_delete=PROTECT, related_name='+')
    number = IntegerField(default=2)
    max_usage_in_minutes = IntegerField(null=True)
    time_to_reach_in_minutes = IntegerField(null=True)

    def __str__(self):
        return self.station.name + " (" + str(self.number) + "x " + str(self.max_usage_in_minutes) + ", " + str(
            self.time_to_reach_in_minutes) + ")"


class VehicleType(Model):
    """From a VehicleType any number of vehicles can be created. VehicleType defines the "static" costs of a Vehicle, while the Vehicles class contains the parameters of the instance"""
    name = CharField(max_length=127)
    vocal_name = CharField(max_length=255)
    workshop_categorie = ForeignKey(WorkshopCategory, on_delete=PROTECT)
    vmax = IntegerField()
    total_price = DecimalField(max_digits=12, decimal_places=2)
    cost_per_km = DecimalField(max_digits=12, decimal_places=6)
    cost_per_hour = DecimalField(max_digits=12, decimal_places=6)
    multi_head_limit = IntegerField()
    cargo_tons_limit = IntegerField()

    def __str__(self):
        return self.name + " (" + self.vocal_name + ")"


class LeasingMode(Model):
    """yearly and weekly costs to own a vehicle"""
    name = CharField(max_length=127)
    vocal_name = CharField(max_length=255)
    factor_yearly = DecimalField(max_digits=6, decimal_places=5)
    factor_weekly = DecimalField(max_digits=6, decimal_places=5)

    def __str__(self):
        return self.name


class Plan(Model):
    """Class to hold a file with the plan of an application an attach it to a tender"""
    creator = ForeignKey(Company, on_delete=PROTECT)
    file = FileField()
    tender = ForeignKey(Tender, on_delete=PROTECT)  # TODO should be optional
    route = ForeignKey(Route, on_delete=PROTECT, null=True)  # plan should be active if it has a route

    def __str__(self):
        return "" + self.id.__str__() + self.tender.__str__() + " (" + self.creator.abbrev + ")"


class Vehicle(Model):
    """The Vehicle class is for "instances" of vehicles. Every instance has a VehicleClass, a leasing_mode and an
    owner. """
    plan = ForeignKey(Plan, null=True, on_delete=SET_NULL)
    vtype = ForeignKey(VehicleType, on_delete=PROTECT)
    owner = ForeignKey(Company, on_delete=PROTECT)
    leasing_mode = ForeignKey(LeasingMode, on_delete=PROTECT)
    leased_since = DateTimeField()

    def __str__(self):
        return self.vtype.name + "-" + self.id


class Criterion(Model):
    """Ciriterion to determine the ranking of tender applications"""
    tender = ForeignKey(Tender, on_delete=CASCADE)
    name = CharField(max_length=127)
    weight = DecimalField(max_digits=12, decimal_places=10)

    def __str__(self):
        return self.name


class Track(Model):
    """Railway line which can be used in tenders resp. which are allows to used in tender applications"""
    tender = ForeignKey(Tender, on_delete=CASCADE)
    start = ForeignKey(Station, related_name='start_of', on_delete=PROTECT)  # TODO perhaps remove backward relation?
    end = ForeignKey(Station, related_name='end_of', on_delete=PROTECT)  # TODO perhaps remove backward relation?
    description = CharField(max_length=255)  # e.g. via or name
    ttype = CharField(max_length=2, choices=Route.TYPE_CHOICES)
    length = DecimalField(max_digits=12, decimal_places=6)
    price = DecimalField(max_digits=12, decimal_places=2)
    tracks = IntegerField()
    travel_time_in_minutes = IntegerField()
    min_speed = IntegerField()

    def __str__(self):
        return self.tender.id + " " + self.start.name + " -> " + self.end.name


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
    FREQUENCY_CHOICES = (
        (ONCE, 'once'),
        (HOURLY, 'hourly'),
        (DAILY, 'daily'),
    )
    PASSENGERS = "PAS"
    CARGO = "CGO"
    TYPE_CHOICES = (
        (PASSENGERS, 'PAS'),
        (CARGO, 'CGO'),
    )
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
        days = "".join([("X" if self.mon else "O"),
                        ("X" if self.tue else "O"),
                        ("X" if self.wed else "O"),
                        ("X" if self.thu else "O"),
                        ("X" if self.fri else "O"),
                        "|",
                        ("X" if self.sat else "O"),
                        ("X" if self.sun else "O"),
                        ])
        return str(self.line.tender.id) + ": " + self.line.name + " " + days + " " + str(self.starttime) + "-" + str(
            self.endtime) + " " + str(
            self.frequency) + " " + self.orgin.name + "->" + self.destination.name + "(" + str(
            self.demand) + " " + self.ttype + ")"
