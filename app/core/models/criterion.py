from django.db.models import Model, ForeignKey, CASCADE, CharField, DecimalField

from core.models.tender import Tender


class Criterion(Model):
    """Criterion to determine the ranking of tender applications"""
    tender = ForeignKey(Tender, on_delete=CASCADE)
    name = CharField(max_length=127)
    weight = DecimalField(max_digits=5, decimal_places=2)
    description = CharField(max_length=511, null=True)
    def __str__(self):
        return self.name
