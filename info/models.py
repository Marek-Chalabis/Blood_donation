from django.db import models
from django.core.validators import RegexValidator
from django.utils import timezone
from django.urls import reverse
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from phonenumber_field.modelfields import PhoneNumberField
from datetime import date
from django.core.exceptions import ValidationError


class Patient(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    gender = models.CharField(max_length=20, choices=(('male', 'male'), ('female', 'female')))
    pesel = models.BigIntegerField(unique=True)
    blood_group = models.CharField(max_length=10,
                                   choices=(('0 Rh+', '0 Rh+'), ('A Rh+', 'A Rh+'), ('B Rh+', 'B Rh+'),
                                            ('AB Rh+', 'AB Rh+'), ('0 Rh-', '0 Rh-'), ('A Rh-', 'A Rh-'),
                                            ('B Rh-', 'B Rh-'), ('AB Rh-', 'AB Rh-')))
    email = models.EmailField(max_length=50, blank=True, null=True, unique=True)
    phone_number = PhoneNumberField(blank=False, default='+48', unique=True)
    date_of_register = models.DateField(default=timezone.now)
    medical_staff = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def get_absolute_url(self):
        return reverse('blood-donation', kwargs={'donor_id': self.id})

    def formatted_phone_number(self):
        phone_number = str(self.phone_number)
        return f'{phone_number[:-9]} {phone_number[-9:-6]} {phone_number[-6:-3]} {phone_number[-3:]}'

    def donor_status(self):
        """
        Returns status of donor depends of given blood and gender
        """
        litres_of_blood = self.donation_set.count() * 0.45
        if litres_of_blood < 5:
            return 'Beginner Donor'
        elif (self.gender == 'male' and litres_of_blood >= 18) or \
                (self.gender == 'female' and litres_of_blood >= 15):
            return 'Distinguished Honorary Blood Donor of the 1st degree'
        elif (self.gender == 'male' and 18 > litres_of_blood >= 12) or \
                (self.gender == 'female' and 15 > litres_of_blood >= 10):
            return 'Distinguished Honorary Blood Donor of the 2st degree'
        elif (self.gender == 'male' and 12 > litres_of_blood >= 6) or \
                (self.gender == 'female' and 10 > litres_of_blood >= 5):
            return 'Distinguished Honorary Blood Donor of the 3st degree'
        else:
            return 'Never donated'

    def can_donate(self):
        number_of_days_from_last_donate = (date.today() - self.donation_set.all().last().date_of_donation).days
        if number_of_days_from_last_donate >= 90:
            donor_can_donate = 'Yes'
        else:
            donor_can_donate = f'No ({90 - number_of_days_from_last_donate} days left)'
        return donor_can_donate

    def given_blood_litres(self):
        return self.donation_set.count() * 0.45

    def __str__(self):
        return f'{self.first_name} {self.last_name}({self.pesel})'


class Donation(models.Model):
    medical_staff = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    patient = models.ForeignKey(Patient, on_delete=models.PROTECT)
    date_of_donation = models.DateField(default=timezone.now)
    accept_donate = models.BooleanField()
    refuse_information = models.TextField(null=True, blank=True)

    def clean(self):
        if self.accept_donate is False and self.refuse_information == '':
            raise ValidationError('If you refuse donation, write why')

    def __str__(self):
        return f'Patient-{self.patient.pesel} Staff-{self.medical_staff.first_name} ' \
               f'{self.medical_staff.last_name} data-{self.date_of_donation}'
