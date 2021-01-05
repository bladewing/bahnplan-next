from django.db import models
from django.contrib.auth import get_user_model

#### Probably not needed since the Django User Model brings enough with it.
#
#class BPUser(models.Model):
#    """extention for django-included user from django.contrib.auth.models"""
#    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)
#    #accepted = models.BooleanField # Unnoetig, da ueber zugriffslevel abbildbar.
#

class Company(models.Model):
    """company, to be owned by an user"""
    name = models.CharField(max_length=255)
    abbrev = models.CharField(max_length=127)
    ownership = models.ManyToManyField(get_user_model()) # unsure, if this will work, but you shouldn't reference the user model directly: See https://github.com/PyCQA/pylint-django/issues/278

class Route(models.Model):
    """The routes, can be operated by a company"""
    CARGO = "CG"
    LOCAL = "LO"
    INTERCITY = "IC"
    TYPE_CHOICES = (
        (CARGO, 'Cargo'),
        (LOCAL, 'Local'),
        (INTERCITY, 'Intercity'),
    )
    operator = models.ForeignKey(Company, on_delete=models.SET_NULL)
    name = models.CharField(max_length=127)
    type = models.CharField(max_length=2, choices=TYPE_CHOICES)
    revenue_per_week = models.DecimalField(max_digits=None, decimal_places=2)
    start_date = models.DateTimeField
    end_date = models.DateTimeField

class Station(models.Model):
    """Database-Represention of a station. Name has to be unique"""
    name = models.CharField(max_length=255, unique=True)

class Workshop(models.Model):
    name = models.CharField(max_length=255)
    station = models.ForeignKey(Station, on_delete=models.PROTECT)

class WorkshopCategory(models.Model):
    name = models.CharField(max_length=255)
    vocal_name = models.CharField(max_length=255)

class Tender(models.Model):
    route = models.ForeignKey(Route, on_delete=models.PROTECT)
    text = models.TextField
    start_date = models.DateTimeField
    end_date = models.DateTimeField
    workshops = models.ManyToManyField(Workshop)

class TrackLimit(models.Model):
    tender = models.ForeignKey(Tender, on_delete=models.CASCADE)
    station = models.ForeignKey(Station, on_delete=models.PROTECT)
    number = models.IntegerField
    max_usage_in_minutes = models.IntegerField
    time_to_reach_in_minutes = models.IntegerField

class VehicleType(models.Model):
    name = models.CharField(max_length=127)
    vocal_name = models.CharField(max_length=255)
    workshop_categorie = models.ForeignKey(WorkshopCategory, on_delete=models.PROTECT)
    vmax = models.IntegerField(max_length=4)
    total_price = models.DecimalField(max_digits=None, decimal_places=2)
    cost_per_km = models.DecimalField(max_digits=None, decimal_places=10)
    cost_per_hour = models.DecimalField(max_digits=None, decimal_places=10)
    multi_head_limit = models.IntegerField()
    cargo_tons_limit = models.IntegerField()

class LeasingMode(models.Model):
    name = models.CharField(max_length=127)
    vocal_name = models.CharField(max_length=255)
    factor_yearly = models.DecimalField(max_digits=None, decimal_places=10)
    factor_monthly = models.DecimalField(max_digits=None, decimal_places=10)

class Plan(models.Model):
    creator = models.ForeignKey(Company, on_delete=models.PROTECT)
    file = models.FileField()
    tender = models.ForeignKey(Tender, on_delete=models.PROTECT) #should be optional
    route = models.ForeignKey(Route, on_delete=models.PROTECT) #plan should be active if it has a route

class Vehicle(models.Model):
    plan = models.ForeignKey(Plan, on_delete=models.SET_NULL)
    type = models.ForeignKey(VehicleType, on_delete=models.PROTECT)
    owner = models.ForeignKey(Company, on_delete=models.PROTECT)
    leasing_mode = models.ForeignKey(LeasingMode, on_delete=models.PROTECT)
    leased_since = models.DateTimeField

class Criterion(models.Model):
    tender = models.ForeignKey(Tender, on_delete=models.CASCADE)
    name = models.CharField(max_length=127)
    weight = models.DecimalField(max_digits=None, decimal_places=10)

class Track(models.Model):
    tender = models.ForeignKey(Tender, on_delete=models.CASCADE)
    start = models.ForeignKey(Station, on_delete=models.PROTECT)
    end = models.ForeignKey(Station, on_delete=models.PROTECT)
    description = models.CharField(max_length=255) # e.g. via or name
    type = models.CharField(max_lenght=2, choices=Route.TYPE_CHOICES)
    length = models.DecimalField(max_digits=None, decimal_places=6)
    price = models.DecimalField(max_digits=None, decimal_places=2)
    tracks = models.IntegerField(max_length=3)
    travel_time_in_minutes = models.IntegerField()
    min_speed = models.IntegerField()

class TransportRequirement(models.Model):
    tender = models.ForeignKey(Tender, on_delete=models.CASCADE)
    orgin = models.ForeignKey(Station, on_delete=models.PROTECT)
    destination = models.ForeignKey(Station, on_delete=models.PROTECT)
