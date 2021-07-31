# Create your model here.
from django.contrib.auth.models import User
from django.db import models

from core.models.company import Company


class Player(models.Model):
    user = models.OneToOneField(User, related_name="player", on_delete=models.CASCADE)
    active_company = models.ForeignKey(Company, on_delete=models.PROTECT, blank=True, null=True)

    def get_companies(self):
        return Company.objects.filter(ownership=self.user)
