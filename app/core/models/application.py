from django.contrib.auth import get_user_model

class Application (models.Model):
    tender = models.ForeignKey(Tender, on_delete=models.CASCADE)
    company = models.ForeignKey(get_user_model, on_delete=SET_NULL)
    ulp = models.FileField(_(""), upload_to=None, max_length=100) #TODO

    class Meta:
        verbose_name = _("Application")
        verbose_name_plural = _("s")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("_detail", kwargs={"pk": self.pk})
)