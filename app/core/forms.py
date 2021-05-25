from django import forms

from core.models import Company


class CompanyCreationForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = ('name', 'abbrev')
