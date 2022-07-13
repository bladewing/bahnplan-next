from django.db import models
from core.models.tender import Tender
from core.models.company import Company
from core.models.criterionvalue import CriterionValue
from django.conf import settings
from django.contrib.auth import get_user_model
import os
from datetime import timezone
import datetime

class Application (models.Model):
    tender = models.ForeignKey(Tender, on_delete=models.SET_NULL, null=True)
    company = models.ForeignKey(Company, on_delete=models.SET_NULL, null=True)
    ulp = models.FilePathField(path=settings.ULP_UPLOAD_DIR) #TODO
    criteria = models.ManyToManyField(CriterionValue)
    submissiontime = models.DateTimeField()
    user = get_user_model()

    class Meta:
        verbose_name = "Application"
        verbose_name_plural = "Applications"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("_detail", kwargs={"pk": self.pk})

    @classmethod
    def create_application(cls, tender, ulp, criteria_dict, active_company, active_user):
        new_application = Application(tender=tender, company=active_company, submissiontime = datetime.datetime.now(), user=active_user)
        new_application.save()
        for criterion in criteria_dict:
            new_criterion = CriterionValue(criterion=criterion, value=criteria_dict[criterion])
            new_crierion.save()
            new_application.criteria.add(new_criterion)
        #TODO handle ulp uploaded file.
        
        #check if folder for tender exist, if not create it
        uploaddir = os.path.join(settings.ULP_UPLOAD_DIR, tender.id)
        if not os.path.exist(uploaddir):
            os.makedir(uploaddir)
   
        # Getting the current date and time
        dt = datetime.datetime.now(timezone.utc)
        utc_time = dt.replace(tzinfo=timezone.utc)
        utc_timestamp = utc_time.timestamp()
        utc_timestamp = utc_timestamp.split('.')[0]

        #TODO Route hasn't a short name, probably add it (e.g. KBS123.45) and add it to the filename
        uploadfile = uploaddir.join(tender.id+'/'+tender.route.type+'_'+tender.id+'_'+active_company.id+'_'+utc_timestamp)
        
        with open(uploadfile, 'wb+') as destination:
            for chunk in ulp.chunks():
                destination.write(chunk)
        
        #TODO 3. add file reference to application object
        self.ulp = uploadfile
        new_application.save()

