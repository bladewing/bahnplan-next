from django.db.models import Model, CharField, DecimalField


class LeasingMode(Model):
    """yearly and weekly costs to own a vehicle"""
    name = CharField(max_length=127)
    factor_yearly = DecimalField(max_digits=4, decimal_places=2)
    factor_weekly = DecimalField(max_digits=4, decimal_places=2)

    def __str__(self):
        return self.name
