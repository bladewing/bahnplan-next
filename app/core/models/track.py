from django.db.models import Model, ForeignKey, CASCADE, PROTECT, CharField, DecimalField, IntegerField

from core.models import Tender, Station, Route


class Track(Model):
    """Railway line which can be used in tenders resp. which are allows to used in tender applications"""
    tender = ForeignKey(Tender, on_delete=CASCADE)
    start = ForeignKey(Station, related_name='start_of', on_delete=PROTECT)
    end = ForeignKey(Station, related_name='end_of', on_delete=PROTECT)
    description = CharField(max_length=255, blank=True, null=True)  # e.g. via or name
    type = CharField(max_length=2, choices=Route.TYPE_CHOICES)
    length = DecimalField(max_digits=12, decimal_places=6)
    price = DecimalField(max_digits=12, decimal_places=2)
    tracks = IntegerField()
    travel_time_in_minutes = IntegerField()
    min_speed = IntegerField()

    def __str__(self):
        return f"{self.tender.id} {self.start.name} -> {self.end.name}"
