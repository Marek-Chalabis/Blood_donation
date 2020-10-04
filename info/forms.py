from django import forms
from django.forms import ModelForm
from localflavor.pl.forms import PLPESELField

from .models import Donation, Patient


class PatientForm(ModelForm):
    pesel = PLPESELField()

    class Meta:
        model = Patient
        fields = "__all__"
        exclude = ["date_of_register", "registered_by"]


class DonationForm(ModelForm):
    class Meta:
        model = Donation
        fields = "__all__"
        exclude = ["medical_staff", "patient", "date_of_donation"]


class InfoForDonor(forms.Form):
    pesel = forms.IntegerField()
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)


class UpdatePatientForm(ModelForm):
    pesel = PLPESELField()

    class Meta:
        model = Patient
        fields = "__all__"
        exclude = ["registered_by", "date_of_register"]
