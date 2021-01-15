from django.contrib.auth import get_user_model
from django.db.models import *

# Probably not needed since the Django User Model brings enough with it.
#
# class BPUser(Model):
#    """extension for django-included user from django.contrib.auth.models"""
#    user = OneToOneField(get_user_model(), on_delete=CASCADE)
#    #accepted = BooleanField # Unnoetig, da ueber zugriffslevel abbildbar.
#
from django.utils.timezone import now


class Company(Model):
    """company, to be owned by an user"""
    name = CharField(max_length=255)
    abbrev = CharField(max_length=127)
    ownership = ManyToManyField(
        get_user_model())

    # unsure, if this will work, but you shouldn't reference the user model directly:
    # See https://github.com/PyCQA/pylint-django/issues/278

    def __str__(self):
        return self.name + ' (' + self.abbrev + ')'


class Route(Model):
    """The routes, can be operated by a company"""
    CARGO = "CG"
    LOCAL = "LO"
    INTERCITY = "IC"
    TYPE_CHOICES = (
        (CARGO, 'Cargo'),
        (LOCAL, 'Local'),
        (INTERCITY, 'Intercity'),
    )
    operator = ForeignKey(Company, null=True, on_delete=SET_NULL)
    name = CharField(max_length=127)
    type = CharField(max_length=2, choices=TYPE_CHOICES)
    revenue_per_week = DecimalField(max_digits=17, decimal_places=2)
    start_date = DateTimeField(default=now)
    end_date = DateTimeField()


class Station(Model):
    """Database-Represention of a station. Name has to be unique"""
    name = CharField(max_length=255, unique=True)


class Workshop(Model):
    name = CharField(max_length=255)
    station = ForeignKey(Station, on_delete=PROTECT)


class WorkshopCategory(Model):
    name = CharField(max_length=255)
    vocal_name = CharField(max_length=255)


class Tender(Model):
    route = ForeignKey(Route, on_delete=PROTECT)
    text = TextField
    start_date = DateTimeField
    end_date = DateTimeField
    workshops = ManyToManyField(Workshop)


class TrackLimit(Model):
    tender = ForeignKey(Tender, on_delete=CASCADE)
    station = ForeignKey(Station, on_delete=PROTECT)
    number = IntegerField
    max_usage_in_minutes = IntegerField
    time_to_reach_in_minutes = IntegerField


class VehicleType(Model):
    name = CharField(max_length=127)
    vocal_name = CharField(max_length=255)
    workshop_categorie = ForeignKey(WorkshopCategory, on_delete=PROTECT)
    vmax = IntegerField()
    total_price = DecimalField(max_digits=10, decimal_places=2)
    cost_per_km = DecimalField(max_digits=5, decimal_places=2)
    cost_per_hour = DecimalField(max_digits=6, decimal_places=2)
    multi_head_limit = IntegerField()
    cargo_tons_limit = IntegerField()


class LeasingMode(Model):
    name = CharField(max_length=127)
    vocal_name = CharField(max_length=255)
    factor_yearly = DecimalField(max_digits=6, decimal_places=5)
    factor_weekly = DecimalField(max_digits=6, decimal_places=5)


class Plan(Model):
    creator = ForeignKey(Company, on_delete=PROTECT)
    file = FileField()
    tender = ForeignKey(Tender, on_delete=PROTECT)  # should be optional
    route = ForeignKey(Route, on_delete=PROTECT)  # plan should be active if it has a route


class Vehicle(Model):
    plan = ForeignKey(Plan, null=True, on_delete=SET_NULL)
    type = ForeignKey(VehicleType, on_delete=PROTECT)
    owner = ForeignKey(Company, on_delete=PROTECT)
    leasing_mode = ForeignKey(LeasingMode, on_delete=PROTECT)
    leased_since = DateTimeField


class Criterion(Model):
    tender = ForeignKey(Tender, on_delete=CASCADE)
    name = CharField(max_length=127)
    weight = DecimalField(max_digits=10, decimal_places=2)


class Track(Model):
    tender = ForeignKey(Tender, on_delete=CASCADE)
    start = ForeignKey(Station, related_name='start_of', on_delete=PROTECT)
    end = ForeignKey(Station, related_name='end_of', on_delete=PROTECT)
    description = CharField(max_length=255)  # e.g. via or name
    type = CharField(max_length=2, choices=Route.TYPE_CHOICES)
    length = DecimalField(max_digits=10, decimal_places=6)
    price = DecimalField(max_digits=5, decimal_places=2)
    tracks = IntegerField()
    travel_time_in_minutes = IntegerField()
    min_speed = IntegerField()


class TransportRequirement(Model):
    tender = ForeignKey(Tender, related_name='requirements', on_delete=CASCADE)
    orgin = ForeignKey(Station, related_name='origin_for', on_delete=PROTECT)
    destination = ForeignKey(Station, related_name='destination_for', on_delete=PROTECT)
