from django import forms

from core.models.company import Company


class CompanyCreationForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = ('name', 'abbrev')
