from django.db.models import Model, ForeignKey, SET_NULL, PROTECT, DateField

from core.models import Company
from core.models.leasing_mode import LeasingMode
from core.models.plan import Plan
from core.models.vehicle_type import VehicleType


class Vehicle(Model):
    """The Vehicle class is for "instances" of vehicles. Every instance has a VehicleClass, a leasing_mode and an
    owner. """
    plan = ForeignKey(Plan, null=True, on_delete=SET_NULL)
    type = ForeignKey(VehicleType, on_delete=PROTECT)
    owner = ForeignKey(Company, on_delete=PROTECT)
    leasing_mode = ForeignKey(LeasingMode, on_delete=PROTECT)
    leased_since = DateField(null=False)

    def __str__(self):
        return f"{self.type.name}-{self.id:03d}"
