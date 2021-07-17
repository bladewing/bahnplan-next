from django.db import models

# Create your model here.
from django.contrib.auth.models import User

from core.models.company import Company


class Player(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    activecompany = models.ForeignKey(Company, on_delete=models.PROTECT, null=True)

    def get_companies(self):
        return Company.objects.filter(ownership=self.user)
