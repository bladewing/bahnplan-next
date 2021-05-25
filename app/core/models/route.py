from django.db.models import Model, ForeignKey, SET_NULL, CharField, DecimalField, DateTimeField

from core.models import Company


class Route(Model):
    """The routes, can be operated by a company"""

    CARGO = "CG"
    LOCAL = "LO"
    LONG_DISTANCE = "IC"
    TYPE_CHOICES = (
        (CARGO, 'Cargo'),
        (LOCAL, 'Local'),
        (LONG_DISTANCE, 'Long Distance'),
    )
    operator = ForeignKey(Company, null=True, blank=True, on_delete=SET_NULL)
    name = CharField(max_length=127)
    type = CharField(max_length=2, choices=TYPE_CHOICES)
    revenue_per_week = DecimalField(max_digits=17, decimal_places=2, blank=True, null=True)
    start_date = DateTimeField(null=True, blank=True)  # was default=now, I think this would't be a good design decision
    end_date = DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.type + " " + self.name + " (" + self.operator.name + ")"
