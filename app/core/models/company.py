from django.contrib.auth import get_user_model
from django.core.validators import MinLengthValidator
from django.db.models import Model, CharField, ManyToManyField, DateField


class Company(Model):
    name = CharField(max_length=255, validators=[MinLengthValidator(1)], default=None, unique=True)
    abbrev = CharField(max_length=8, validators=[MinLengthValidator(1)], unique=True)
    creation_date = DateField(auto_now_add=True)
    ownership = ManyToManyField(get_user_model())

    def __str__(self):
        return self.name + ' (' + self.abbrev + ')'

    @staticmethod
    def create_owned_company(name, abbrev, owners):
        new_company = Company(name=name, abbrev=abbrev)
        new_company.save()

        if not isinstance(owners, list):
            new_company.ownership.add(owners)
            new_company.save()
        else:
            for owner in owners:
                new_company.ownership.add(owner)
            new_company.save()
        return new_company
