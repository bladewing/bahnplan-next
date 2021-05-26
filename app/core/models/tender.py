from django.db.models import *

from core.models.route import Route
from core.models.workshop import Workshop

class Tender(Model):
    """Tenders where Users can apply for"""
    route = ForeignKey(Route, on_delete=PROTECT)
    text = TextField(null=True)
    start_date = DateTimeField(null=True, blank=True)
    end_date = DateTimeField(null=True, blank=True)
    workshops = ManyToManyField(Workshop)

    def __str__(self):
        return self.route.__str__()