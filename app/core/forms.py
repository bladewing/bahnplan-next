from django import forms

from .models import Company

class CompanyCreationForm(forms.ModelForm):

    class Meta:
        model = Company
        fields = ('name', 'abbrev')
