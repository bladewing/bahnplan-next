from django.db.models import Model, CharField


class Station(Model):
    """Database-Representation of a station. Name has to be unique"""
    name = CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name
