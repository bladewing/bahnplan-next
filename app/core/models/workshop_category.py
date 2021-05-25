from django.db.models import Model, IntegerField


class WorkshopCategory(Model):
    """WorkShopCategories defines, which vehicles can be services in which workshops"""
    category = IntegerField(blank=False)

    def __str__(self):
        return 'Kategorie %d' % self.category
