from django.db import models
from core.models.tender import Tender
from core.models.company import Company
from core.models.criterionvalue import CriterionValue
from django.conf import settings

class Application (models.Model):
    tender = models.ForeignKey(Tender, on_delete=models.SET_NULL, null=True)
    company = models.ForeignKey(Company, on_delete=models.SET_NULL, null=True)
    ulp = models.FilePathField(path=settings.ULP_UPLOAD_DIR) #TODO
    criterions = models.ManyToManyField(CriterionValue)

    class Meta:
        verbose_name = "Application"
        verbose_name_plural = "s"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("_detail", kwargs={"pk": self.pk})
