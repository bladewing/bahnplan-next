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
    def __str__(self):
        return self.abbrev

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
    operator = models.ForeignKey(Company, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=127)
    type = models.CharField(max_length=2, choices=TYPE_CHOICES)
    revenue_per_week = models.DecimalField(max_digits=12, decimal_places=2)
    start_date = models.DateTimeField
    end_date = models.DateTimeField
    def __str__(self):
        return self.type + " " + self.name + " (" + self.operator + ")"
    

class Station(models.Model):
    """Database-Represention of a station. Name has to be unique"""
    name = models.CharField(max_length=255, unique=True)
    def __str__(self):
        return self.name
    

class WorkshopCategory(models.Model):
    """WorkShopCategories defines, which vehicles can be services in which workshops"""
    name = models.CharField(max_length=255)
    vocal_name = models.CharField(max_length=255)
    def __str__(self):
        return self.vocal_name + " ("+self.name + ")"
    

class Workshop(models.Model):
    """Workshops, have to be attached to an existing station and can have WorkshopCategories"""
    name = models.CharField(max_length=255)
    station = models.ForeignKey(Station, on_delete=models.PROTECT)
    categories = models.ManyToManyField(WorkshopCategory)
    def __str__(self):
        catstring = " ("
        for category in self.categories.all():
            catstring = catstring + category.name
        catstring = catstring + ")"
        return self.name + self.station + catstring
    

class Tender(models.Model):
    """Tenders where Users can apply to"""
    route = models.ForeignKey(Route, on_delete=models.PROTECT)
    text = models.TextField
    start_date = models.DateTimeField
    end_date = models.DateTimeField
    workshops = models.ManyToManyField(Workshop)
    def __str__(self):
        return self.route.__str__()

class TrackLimit(models.Model):
    """The usage of a station by each tender can be limited with TrackLimit"""
    tender = models.ForeignKey(Tender, on_delete=models.CASCADE)
    station = models.ForeignKey(Station, on_delete=models.PROTECT, related_name='+')
    number = models.IntegerField
    max_usage_in_minutes = models.IntegerField
    time_to_reach_in_minutes = models.IntegerField
    def __str__(self):
        return self.station.name + " (" + self.number + "x " + self.max_usage_in_minutes + ", " + self.time_to_reach_in_minutes + ")"

class VehicleType(models.Model):
    """From a VehicleType any number of vehicles can be created. VehicleType defines the "static" costs of a Vehicle, while the Vehicles class contains the parameters of the instance"""
    name = models.CharField(max_length=127)
    vocal_name = models.CharField(max_length=255)
    workshop_categorie = models.ForeignKey(WorkshopCategory, on_delete=models.PROTECT)
    vmax = models.IntegerField()
    total_price = models.DecimalField(max_digits=12, decimal_places=2)
    cost_per_km = models.DecimalField(max_digits=12, decimal_places=6)
    cost_per_hour = models.DecimalField(max_digits=12, decimal_places=6)
    multi_head_limit = models.IntegerField()
    cargo_tons_limit = models.IntegerField()
    def __str__(self):
        return self.name + " (" + self.vocal_name + ")"
    

class LeasingMode(models.Model):
    """yearly and weekly costs to own a vehicle"""
    name = models.CharField(max_length=127)
    vocal_name = models.CharField(max_length=255)
    factor_yearly = models.DecimalField(max_digits=12, decimal_places=10)
    factor_weekly = models.DecimalField(max_digits=12, decimal_places=10)
    def __str__(self):
        return self.name

class Plan(models.Model):
    """Class to hold a file with the plan of an application an attach it to a tender"""
    creator = models.ForeignKey(Company, on_delete=models.PROTECT)
    file = models.FileField()
    tender = models.ForeignKey(Tender, on_delete=models.PROTECT) #should be optional
    route = models.ForeignKey(Route, on_delete=models.PROTECT) #plan should be active if it has a route
    def __str__(self):
        return self.id + self.tender.__str__() + " (" + self.creator.abbrev + ")"

class Vehicle(models.Model):
    """The Vehicle class is for "instances" of vehicles. Every instance has a VehicleClass, a leasing_mode and an owner."""
    plan = models.ForeignKey(Plan, on_delete=models.SET_NULL, null=True)
    type = models.ForeignKey(VehicleType, on_delete=models.PROTECT)
    owner = models.ForeignKey(Company, on_delete=models.PROTECT)
    leasing_mode = models.ForeignKey(LeasingMode, on_delete=models.PROTECT)
    leased_since = models.DateTimeField
    def __str__(self):
        return self.type.name + "-" + self.id
    

class Criterion(models.Model):
    """Ciriterion to determine the ranking of tender applications"""
    tender = models.ForeignKey(Tender, on_delete=models.CASCADE)
    name = models.CharField(max_length=127)
    weight = models.DecimalField(max_digits=12, decimal_places=10)
    def __str__(self):
        return self.name

class Track(models.Model):
    """Railway line which can be used in tenders resp. which are allows to used in tender applications"""
    tender = models.ForeignKey(Tender, on_delete=models.CASCADE)
    start = models.ForeignKey(Station, on_delete=models.PROTECT, related_name='+')
    end = models.ForeignKey(Station, on_delete=models.PROTECT, related_name='+')
    description = models.CharField(max_length=255) # e.g. via or name
    type = models.CharField(max_length=2, choices=Route.TYPE_CHOICES)
    length = models.DecimalField(max_digits=12, decimal_places=6)
    price = models.DecimalField(max_digits=12, decimal_places=2)
    tracks = models.IntegerField()
    travel_time_in_minutes = models.IntegerField()
    min_speed = models.IntegerField()
    def __str__(self):
        return self.tender.id + " " + self.start.name + " -> " + self.end.name

class TransportRequirement(models.Model):
    """Demand which have to be transported to send a valid tender application"""
    tender = models.ForeignKey(Tender, on_delete=models.CASCADE)
    orgin = models.ForeignKey(Station, on_delete=models.PROTECT, related_name='+')
    destination = models.ForeignKey(Station, on_delete=models.PROTECT, related_name='+')
    def __str__(self):
        return self.tender.id + ": " + self.orgin.name + "->" + self.destination.name
    
