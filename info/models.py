import datetime
from datetime import date

from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import F, Value
from django.db.models.functions import Concat
from django.urls import reverse
from django.utils import timezone
from phonenumber_field.modelfields import PhoneNumberField


class Patient(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    gender = models.CharField(
        max_length=20, choices=(("male", "male"), ("female", "female"))
    )
    pesel = models.BigIntegerField(unique=True)
    blood_group = models.CharField(
        max_length=10,
        choices=(
            ("0 Rh+", "0 Rh+"),
            ("A Rh+", "A Rh+"),
            ("B Rh+", "B Rh+"),
            ("AB Rh+", "AB Rh+"),
            ("0 Rh-", "0 Rh-"),
            ("A Rh-", "A Rh-"),
            ("B Rh-", "B Rh-"),
            ("AB Rh-", "AB Rh-"),
        ),
    )
    email = models.EmailField(max_length=50, blank=True, null=True, unique=True)
    phone_number = PhoneNumberField(blank=False, default="+48", unique=True)
    date_of_register = models.DateField(default=datetime.date.today)
    registered_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}({self.pesel})"

    def get_absolute_url(self):
        return reverse("blood-donation", kwargs={"donor_id": self.id})

    def formatted_phone_number(self):
        phone_number = str(self.phone_number)
        return f"{phone_number[:-9]} {phone_number[-9:-6]} {phone_number[-6:-3]} {phone_number[-3:]}"

    def last_correct_donation(self):
        # last correct donation
        try:
            return (
                Donation.objects.filter(patient=self, accept_donate=True)
                .values_list("date_of_donation", flat=True)
                .latest("date_of_donation")
            )
        except:
            return None

    def donor_status(self, litres_of_blood=None):
        """
        Returns status of donor depends of given blood and gender
        """

        if litres_of_blood == None:
            litres_of_blood = Patient.given_blood_litres(self)

        if litres_of_blood < 5:
            return "Beginner Donor"
        elif (self.gender == "male" and litres_of_blood >= 18) or (
            self.gender == "female" and litres_of_blood >= 15
        ):
            return "Distinguished Honorary Blood Donor of the 1st degree"
        elif (self.gender == "male" and 18 > litres_of_blood >= 12) or (
            self.gender == "female" and 15 > litres_of_blood >= 10
        ):
            return "Distinguished Honorary Blood Donor of the 2st degree"
        elif (self.gender == "male" and 12 > litres_of_blood >= 6) or (
            self.gender == "female" and 10 > litres_of_blood >= 5
        ):
            return "Distinguished Honorary Blood Donor of the 3st degree"
        else:
            return "Never donated"

    def can_donate(self):
        # checks if donor can donate
        last_donate = Patient.last_correct_donation(self)

        if last_donate is None:
            return "Never donated"
        else:
            days_from_last_donate = (date.today() - last_donate).days
            if days_from_last_donate >= 90:
                return "Yes"
            else:
                return f"No ({days_from_last_donate} days left)"

    def given_blood_litres(self):
        return Donation.objects.filter(patient=self).count() * 0.45

    def medical_worker_responsible_for_register(self):
        full_repr_of_medical = Patient.objects.select_related(
            "registered_by", "registered_by__profile"
        ).get(id=self.id)
        return (
            f"{full_repr_of_medical.registered_by.profile.position} "
            f"{full_repr_of_medical.registered_by.first_name} "
            f"{full_repr_of_medical.registered_by.last_name}"
        )

    def history_of_donation(self):
        # history of donations
        return (
            Donation.objects.filter(patient_id=self.id)
            .select_related("medical_staff", "medical_staff__profile")
            .annotate(
                medic_full_description=Concat(
                    F("medical_staff__profile__position"),
                    Value(" "),
                    F("medical_staff__first_name"),
                    Value(" "),
                    F("medical_staff__last_name"),
                )
            )
            .order_by("-date_of_donation")
        )


class Donation(models.Model):
    medical_staff = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    patient = models.ForeignKey(Patient, on_delete=models.PROTECT)
    date_of_donation = models.DateField(default=datetime.date.today)
    accept_donate = models.BooleanField()
    refuse_information = models.TextField(null=True, blank=True)

    def clean(self):
        if self.accept_donate is False and self.refuse_information == "":
            raise ValidationError("If you refuse donation, write why")

    def __str__(self):
        return (
            f"Patient-{self.patient.pesel} Staff-{self.medical_staff.first_name} "
            f"{self.medical_staff.last_name} data-{self.date_of_donation}"
        )
