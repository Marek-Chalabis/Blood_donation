#  -*- coding: utf-8 -*-
"""
Creates DATABASE for project
"""
import Random_generator
import os
import random
import json
import datetime

# Fill to get json_file adequate to your needs
NUMBER_OF_USERS = 60
NUMBER_OF_PATIENTS = 500
NUMBER_OF_DONATION = 3500


class Patient:
    """
    Creates Patient
    """
    list_of_patients = []

    def __init__(self):
        sex = random.choice(['M', 'F'])
        first_name, last_name = Random_generator.Person.full_name(sex)
        gender = 'male' if sex == 'M' else 'female'
        birth_date = Random_generator.Basic.random_date('1930-01-01', '2000-12-20')
        # make sure that donors are 18+
        date_to_majority = datetime.datetime.strptime(birth_date, "%Y-%m-%d")
        register_day = date_to_majority + datetime.timedelta(days=6575)
        self.first_name = first_name
        self.last_name = last_name
        self.gender = gender
        self.email = Random_generator.Person.email()
        while self.email in [pat.pesel for pat in Patient.list_of_patients]:
            self.email = Random_generator.Person.email()

        self.pesel = Random_generator.Person.pesel(sex, birth_date, True)
        while self.pesel in [pat.pesel for pat in Patient.list_of_patients]:
            self.pesel = Random_generator.Person.pesel(sex, birth_date, True)

        self.date_of_register = register_day.strftime("%Y-%m-%d")
        self.blood_group = random.choices(
            population=['0 Rh+', 'A Rh+', 'B Rh+', 'AB Rh+', '0 Rh-', 'A Rh-', 'B Rh-', 'AB Rh-'],
            weights=[31, 32, 15, 7, 6, 6, 2, 1])[0]
        self.phone_number = Random_generator.Person.phone_number()
        while self.phone_number in [pat.phone_number for pat in Patient.list_of_patients]:
            self.phone_number = Random_generator.Person.phone_number()
        Patient.list_of_patients.append(self)


class Donation:
    """
    Create Donation
    """
    list_of_donations = []
    list_of_patients = []

    def __init__(self, patient):
        self.patient = patient

        if patient not in Donation.list_of_patients:
            self.date_of_donation = patient.date_of_register
            self.accept_donate = random.choices(population=['True', 'False'], weights=[85, 15])[0]
            Donation.list_of_patients.append(self.patient)
        else:
            self.date_of_donation, self.accept_donate = Donation.__date_of_next_donate(self.patient)

        self.refuse_information = None if self.accept_donate == 'True' else Random_generator.Basic.words(
            random.randint(10, 30))
        Donation.list_of_donations.append(self)

    @classmethod
    def __date_of_next_donate(cls, patient_to_find):
        """
        returns date of next donation or remove patient if he cannot donate
        """
        dates = []
        for donation in cls.list_of_donations:
            if donation.patient == patient_to_find:
                dates.append(donation.date_of_donation)
        last_donate = datetime.datetime.strptime(dates[-1], "%Y-%m-%d")

        if (datetime.datetime.today() - last_donate).days < 91:
            correct_date_to_donate = last_donate + datetime.timedelta(
                days=random.randint(1, (datetime.datetime.today() - last_donate).days))
            Patient.list_of_patients.remove(patient_to_find)
            return correct_date_to_donate.strftime("%Y-%m-%d"), "False"
        else:
            correct_date_to_donate = last_donate + datetime.timedelta(days=90)
            date_donate = Random_generator.Basic.random_date(correct_date_to_donate)
            return date_donate, random.choices(population=['True', 'False'], weights=[75, 25])[0]


def folder_for_data():
    """creates folder for dummy_data"""
    FOLDER_FOR_DATA = 'dummy_data'
    path_to_data = os.getcwd() + fr'\{FOLDER_FOR_DATA}'
    try:
        os.makedirs(path_to_data)
    except FileExistsError:
        pass
    return path_to_data


def users_json(path_folder):
    """Create json file for users and saves"""
    json_info = []
    list_username = []
    for i in range(NUMBER_OF_USERS):
        username = Random_generator.Basic.words(1)
        while username in list_username:
            username = Random_generator.Basic.words(1)
        list_username.append(username)
        first_name, last_name = Random_generator.Person.full_name()
        json_info.append({
            'username': Random_generator.Basic.words(1),
            'email': Random_generator.Person.email(),
            'password': Random_generator.Person.password(),
            'first_name': first_name,
            'last_name': last_name
        })
    with open(os.path.join(path_folder, 'users.json'), 'w') as json_file:
        json.dump(json_info, json_file)


def profile_json(path_folder):
    """Create json file for profile and saves"""
    json_info = []
    images = Random_generator.Basic.image(path_folder, 'hospital', 30)
    for i in range(NUMBER_OF_USERS):
        json_info.append({
            'image': random.choice(images),
            'position': random.choice(['doctor', 'resident doctor', 'medical specialist', 'habilitated doctor',
                                       'professor', 'nurse']),
            'branch': random.choice(['Warszawa', 'Lublin', 'Radom', 'Gdynia', 'Kraków']),
        })
    with open(os.path.join(path_folder, 'profile.json'), 'w') as json_file:
        json.dump(json_info, json_file)


def patient_json(path_folder):
    """Create json file for patient and saves"""
    json_info = []
    for i in range(NUMBER_OF_PATIENTS):
        patient = Patient()
        json_info.append({
            'first_name': patient.first_name,
            'email': patient.email,
            'last_name': patient.last_name,
            'gender': patient.gender,
            'pesel': patient.pesel,
            'blood_group': patient.blood_group,
            'phone_number': patient.phone_number,
            'date_of_register': patient.date_of_register,
            # ADD USER IN SHELL
        })
    with open(os.path.join(path_folder, 'patient.json'), 'w') as json_file:
        json.dump(json_info, json_file)


def donation_json(path_folder):
    """Create json file for donation and saves"""
    json_info = []
    for i in range(NUMBER_OF_DONATION):
        donation = Donation(random.choice(Patient.list_of_patients))
        json_info.append({
            # medical_staff ADD IN SHELL
            # patient ADD IN SHELL
            'date_of_donation': donation.date_of_donation,
            'accept_donate': donation.accept_donate,
            'refuse_information': donation.refuse_information,
        })
    with open(os.path.join(path_folder, 'donation.json'), 'w') as json_file:
        json.dump(json_info, json_file)


input('Check numbers at the top of the file'
      '\nPress any key to continue . . .')
print('It will take few seconds depends on amount of generated data...')
path = folder_for_data()
users_json(path)
profile_json(path)
while True:
    try:
        patient_json(path)
        donation_json(path)
        break
    except IndexError:
        print('Refresh....Just Wait. '
              'If this will happen more times you need to lower NUMBER_OF_DONATION or add more to NUMBER OF PATIENTS')
        Patient.list_of_patients.clear()
        Donation.list_of_patients.clear()
        Donation.list_of_donations.clear()
        pass

print('Follow the instructions below'
      '\n===Go to django terminal and write this commends:==='
      '\n\nmanage.py makemigrations'
      '\n\nmanage.py migrate'
      '\n\nmanage.py shell'
      '\n\nimport json;from users.models import *;from info.models import *;from django.contrib.auth.models import User;from django.core.files import File;import random;users_list=[];patient_list=[];'
      '\n\nwith open("dummy_data/users.json") as file_users, open("dummy_data/profile.json") as file_profile, open("dummy_data/patient.json") as file_patient, open("dummy_data/donation.json") as file_donation:    users_json=json.load(file_users);    profile_json=json.load(file_profile);    patient_json=json.load(file_patient);    donation_json=json.load(file_donation);'
      '\n\nfor user, profile_user in zip(users_json, profile_json):     new_user = User(username=user["username"], email=user["email"], password=user["password"], first_name=user["first_name"], last_name=user["last_name"]);     new_user.save();     new_user.profile.position=profile_user["position"];     new_user.save();     new_user.profile.branch=profile_user["branch"];     new_user.save();      new_user.profile.image.save(f"{new_user.username}.jpg", File(open(profile_user["image"], "rb")));     users_list.append(new_user);'
      '\n\nfor patient in patient_json:     new_patient = Patient(first_name=patient["first_name"], last_name=patient["last_name"], gender=patient["gender"], email=patient["email"], pesel=patient["pesel"], blood_group=patient["blood_group"], phone_number=patient["phone_number"], date_of_register=patient["date_of_register"], medical_staff=random.choice(users_list));     new_patient.save();     patient_list.append(new_patient);'
      '\n\nfor donate in donation_json:     new_donation = Donation(medical_staff=random.choice(users_list), patient=random.choice(patient_list), accept_donate=donate["accept_donate"], refuse_information=donate["refuse_information"], date_of_donation=donate["date_of_donation"]);     new_donation.save();'
      '\n\nexit()'
      '\n\nmanage.py createsuperuser'
      '\n\nmanage.py runserver'
      '\n\n===LOOK TO THE TOP===')
