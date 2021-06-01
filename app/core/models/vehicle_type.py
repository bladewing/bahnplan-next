from django.db.models import Model, CharField, ForeignKey, PROTECT, IntegerField, DecimalField

from core.models.workshop_category import WorkshopCategory


class VehicleType(Model):
    """From a VehicleType any number of vehicles can be created. VehicleType defines the "static" costs of a Vehicle,
    while the Vehicles class contains the parameters of the instance """
    name = CharField(max_length=127, unique=True)
    vocal_name = CharField(max_length=255, blank=True)
    workshop_category = ForeignKey(WorkshopCategory, on_delete=PROTECT)
    v_max = IntegerField()
    total_price = DecimalField(max_digits=12, decimal_places=2)
    cost_per_km = DecimalField(max_digits=12, decimal_places=6)
    cost_per_hour = DecimalField(max_digits=12, decimal_places=6)
    multi_head_limit = IntegerField()
    cargo_tons_limit = IntegerField()

    def __str__(self):
        if self.vocal_name != "":
            return f"{self.name} ({self.vocal_name})"
        return f"{self.name}"
