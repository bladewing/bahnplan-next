from django.db.models import Model, ForeignKey, CASCADE, CharField

from core.models.tender import Tender


class Line(Model):
    """Lines are mostly like 'containers' holding different demands for tenders."""
    tender = ForeignKey(Tender, on_delete=CASCADE)
    name = CharField(max_length=127)

    def __str__(self):
        return f"{self.name} ({self.tender.__str__()})"
