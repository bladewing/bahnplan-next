from django.db.models import Model, ForeignKey, PROTECT, FileField

from core.models.company import Company
from core.models.route import Route
from core.models.tender import Tender


class Plan(Model):
    """Class to hold a file with the plan of an application an attach it to a tender"""
    creator = ForeignKey(Company, on_delete=PROTECT)
    file = FileField(upload_to='plans/')
    tender = ForeignKey(Tender, on_delete=PROTECT, null=True)
    route = ForeignKey(Route, on_delete=PROTECT, null=True)  # plan should be active if it has a route

    def __str__(self):
        if self.tender is None:
            return f"{self.id.__str__()} ({self.creator.abbrev})"
        return f"{self.id.__str__()} {self.tender.__str__()} ({self.creator.abbrev})"

    def is_active(self):
        return self.route is not None
