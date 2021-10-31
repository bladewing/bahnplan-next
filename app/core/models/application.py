from django.db import models
from core.models.tender import Tender
from core.models.company import Company
from core.models.criterionvalue import CriterionValue
from django.conf import settings

class Application (models.Model):
    tender = models.ForeignKey(Tender, on_delete=models.SET_NULL, null=True)
    company = models.ForeignKey(Company, on_delete=models.SET_NULL, null=True)
    ulp = models.FilePathField(path=settings.ULP_UPLOAD_DIR) #TODO
    criteria = models.ManyToManyField(CriterionValue)

    class Meta:
        verbose_name = "Application"
        verbose_name_plural = "s"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("_detail", kwargs={"pk": self.pk})

    @classmethod
    def create_application(cls, tender, ulp, criteria_dict, active_company):
        new_application = Application(tender=tender, company=active_company)
        new_application.save()
        for criterion in criteria_dict:
            new_criterion = CriterionValue(criterion=criterion, value=criteria_dict[criterion])
            new_crierion.save()
            new_application.criteria.add(new_criterion)
        #TODO handle ulp uploaded file.
        #1. check if folder for tender exist, if not create it
        #2. copy file to applications folder, rename it to ApplicationID_CompanyAbbrev_UploadTime
        #TODO Route hasn't have a short name, probably add it (e.g. KBS123.45) and add it to the filename
        #3. add file reference to application object

