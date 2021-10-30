from django import forms

from core.models.company import Company
from core.models.application import Application


class CompanyCreationForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = ('name', 'abbrev')

class ApplicationDataForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ('criterions')