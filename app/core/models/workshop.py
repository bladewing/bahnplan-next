from django.db.models import Model, CharField, ForeignKey, PROTECT, ManyToManyField

from core.models.station import Station
from core.models.workshop_category import WorkshopCategory


class Workshop(Model):
    """Workshops, have to be attached to an existing station and can have WorkshopCategories"""
    name = CharField(max_length=255)
    station = ForeignKey(Station, on_delete=PROTECT)
    categories = ManyToManyField(WorkshopCategory)

    def __str__(self):
        category_strings = sorted(map(lambda x: x.category.__str__(), self.categories.all()))
        return self.name + ' in ' + self.station.name + ' (Kategorie ' + ', '.join(category_strings) + ')'
