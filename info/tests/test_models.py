import datetime

import pendulum
import pytest
from django.contrib.auth.models import User
from django.db.models.query import QuerySet
from mixer.backend.django import mixer

from info.models import Patient, Donation


@pytest.mark.django_db
class TestPatient:

    def test_formatted_phone_number(self):
        patient = mixer.blend(Patient, phone_number=+48123456789)
        assert patient.formatted_phone_number() == "48 123 456 789"

    def test_last_correct_donation_accepted(self):
        patient = mixer.blend(Patient)
        donation = mixer.blend(Donation, patient=patient, accept_donate=True)
        assert patient.last_correct_donation() == datetime.date.today()

    def test_last_correct_donation_not_accepted(self):
        patient = mixer.blend(Patient)
        donation = mixer.blend(Donation, patient=patient, accept_donate=False)
        assert patient.last_correct_donation() == None

    def test_given_blood_litres_no_donations(self):
        patient = mixer.blend(Patient)
        donation = mixer.blend(Donation, patient=patient, accept_donate=False)
        assert patient.given_blood_litres() == 0.0

    def test_given_blood_litres_given_donations(self):
        patient = mixer.blend(Patient)
        for _ in range(5):
            donation = mixer.blend(Donation, patient=patient, accept_donate=True)
        assert patient.given_blood_litres() == 2.25

    def test_donor_status_no_given_litres_male(self):
        patient_never_donated = mixer.blend(Patient, gender='male')
        # phone_number is given to make ewry patient unique
        patient_beginner = mixer.blend(Patient, phone_number=1, gender='male')
        for _ in range(5):
            donation = mixer.blend(Donation, patient=patient_beginner, accept_donate=True)
        patient_1st_degree = mixer.blend(Patient, phone_number=2, gender='male')
        for _ in range(50):
            donation = mixer.blend(Donation, patient=patient_1st_degree, accept_donate=True)
        patient_2st_degree = mixer.blend(Patient, phone_number=3, gender='male')
        for _ in range(30):
            donation = mixer.blend(Donation, patient=patient_2st_degree, accept_donate=True)
        patient_3st_degree = mixer.blend(Patient, phone_number=4, gender='male')
        for _ in range(20):
            donation = mixer.blend(Donation, patient=patient_3st_degree, accept_donate=True)
        assert patient_never_donated.donor_status() != patient_beginner.donor_status() != patient_1st_degree.donor_status() != patient_2st_degree.donor_status() != patient_3st_degree.donor_status()

    def test_donor_status_no_given_litres_female(self):
        patient_never_donated = mixer.blend(Patient, gender='female')
        # phone_number is given to make ewry patient unique
        patient_beginner = mixer.blend(Patient, phone_number=1, gender='female')
        for _ in range(5):
            donation = mixer.blend(Donation, patient=patient_beginner, accept_donate=True)
        patient_1st_degree = mixer.blend(Patient, phone_number=2, gender='female')
        for _ in range(50):
            donation = mixer.blend(Donation, patient=patient_1st_degree, accept_donate=True)
        patient_2st_degree = mixer.blend(Patient, phone_number=3, gender='female')
        for _ in range(25):
            donation = mixer.blend(Donation, patient=patient_2st_degree, accept_donate=True)
        patient_3st_degree = mixer.blend(Patient, phone_number=4, gender='female')
        for _ in range(15):
            donation = mixer.blend(Donation, patient=patient_3st_degree, accept_donate=True)
        assert patient_never_donated.donor_status() != patient_beginner.donor_status() != patient_1st_degree.donor_status() != patient_2st_degree.donor_status() != patient_3st_degree.donor_status()

    def test_can_donate_never_donated(self):
        patient = mixer.blend(Patient)
        assert patient.can_donate() == 'Never donated'

    def test_can_donate_cant_donate(self):
        patient = mixer.blend(Patient)
        donation = mixer.blend(Donation, patient=patient, accept_donate=True)
        assert patient.can_donate().startswith('No') is True

    def test_can_donate_can_donate(self):
        patient = mixer.blend(Patient)
        donation = mixer.blend(Donation, patient=patient, accept_donate=True, date_of_donation=pendulum.now().subtract(days=91))
        assert patient.can_donate().startswith('Yes') is True

    def test_medical_worker_responsible_for_register(self):
        user = mixer.blend(User, first_name='test_NAME', last_name='test_LAST_NAME')
        patient = mixer.blend(Patient, registered_by=user)
        assert patient.medical_worker_responsible_for_register() == ' test_NAME test_LAST_NAME'

    def test_history_of_donation(self):
        patient = mixer.blend(Patient)
        assert isinstance(patient.history_of_donation(), QuerySet)


