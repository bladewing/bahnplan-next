from django.db import models
from core.models.criterion import Criterion

class CriterionValue(models.Model):
    criterion = models.ForeignKey(Criterion, on_delete=models.CASCADE)
    value = models.DecimalField(max_digits=12, decimal_places=5)

    def __str__(self):
        return self.criterion.name + ": " + value