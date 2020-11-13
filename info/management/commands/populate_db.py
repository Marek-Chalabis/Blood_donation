import json
import os
import random

from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.core.files import File
from django.core.management.base import BaseCommand

from info.models import *


class Command(BaseCommand):
    help = 'Populate DB'

    def add_arguments(self, parser):
        parser.add_argument('path', type=str, help='Path to folder with data to populate')
        parser.add_argument('-a', '--admin', action='store_true',
                            help='Adds test superuser login: admin password: admin, email: admin@gmail.com')

    def handle(self, *args, **kwargs):
        self.stdout.write("populating DB...")
        path_to_folder = kwargs['path']
        add_super_user = kwargs['admin']

        with open(os.path.join(path_to_folder, "users.json"), 'r') as file_users, \
                open(os.path.join(path_to_folder, "profile.json"), 'r') as file_profile, \
                open(os.path.join(path_to_folder, "patient.json"), 'r') as file_patient, \
                open(os.path.join(path_to_folder, "donation.json"), 'r') as file_donation:
            users_json = json.load(file_users)
            profile_json = json.load(file_profile)
            patient_json = json.load(file_patient)
            donation_json = json.load(file_donation)

        users_list = []
        for user, profile_user in zip(users_json, profile_json):
            new_user = User(username=user["username"],
                            email=user["email"],
                            password=user["password"],
                            first_name=user["first_name"],
                            last_name=user[
                                "last_name"])
            new_user.save()
            new_user.profile.position = profile_user["position"]
            new_user.profile.branch = profile_user["branch"]
            new_user.save()
            new_user.profile.image.save(f"{new_user.username}.jpg", File(open(profile_user["image"], "rb")))
            users_list.append(new_user)

        for patient in patient_json:
            new_patient = Patient(first_name=patient["first_name"],
                                  last_name=patient["last_name"], gender=patient["gender"],
                                  email=patient["email"], pesel=patient["pesel"],
                                  blood_group=patient["blood_group"],
                                  phone_number=patient["phone_number"],
                                  date_of_register=patient["date_of_register"],
                                  registered_by=random.choice(
                                      users_list))
            new_patient.save()

        for donate in donation_json:
            correct_patient = Patient.objects.get(pesel=donate["patient_pesel"])
            new_donation = Donation(medical_staff=random.choice(users_list), patient=correct_patient,
                                    accept_donate=donate["accept_donate"],
                                    refuse_information=donate["refuse_information"],
                                    date_of_donation=donate["date_of_donation"])
            new_donation.save()

        if add_super_user:
            super_user = get_user_model()
            super_user.objects.create_superuser('admin', 'admin@gmail.com', 'admin')
            self.stdout.write("added test admin (login: admin, password: admin, email: admin@gmail.com)")

        self.stdout.write("populating DB complete")
