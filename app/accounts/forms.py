from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

from core.models.leasing_mode import LeasingMode


class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Erforderlich. Muss eine gültige E-Mail-Adresse sein.')

    class Meta:
        model = get_user_model()
        fields = ('username', 'email', 'password1', 'password2',)


# TODO unused for now, needs to know vehicleTypeId also
class VehicleLeaseForm(forms.Form):
    amount = forms.IntegerField(label="Anzahl")
    leasing_mode = forms.ModelChoiceField(queryset=LeasingMode.objects, label="Leasingmodell")
