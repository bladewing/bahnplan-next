from decimal import Decimal

from django.core.validators import MinValueValidator
from django.db.models import Model, DateTimeField, ForeignKey, SET_NULL, DecimalField, CharField

from core.models.company import Company


class Transaction(Model):
    payer = ForeignKey(Company, on_delete=SET_NULL, null=True, blank=True, related_name="paying_to")
    recipient = ForeignKey(Company, on_delete=SET_NULL, null=True, blank=True, related_name="receiving_from")
    timestamp = DateTimeField(auto_now_add=True)
    amount = DecimalField(max_digits=17, decimal_places=2, validators=[MinValueValidator(Decimal('0.01'))])
    reason = CharField(max_length=127)
