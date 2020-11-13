#  -*- coding: utf-8 -*-
"""
Creates DATABASE for project
"""
import datetime
import json
import os
import random

import random_generator

# Fill to get json_file adequate to your needs
NUMBER_OF_USERS = 70
NUMBER_OF_PATIENTS = 1000
NUMBER_OF_DONATION = 7000


class Patient:
    """
    Creates Patient
    """

    list_of_patients = []

    def __init__(self):
        sex = random.choice(["M", "F"])
        first_name, last_name = random_generator.Person.full_name(sex)
        gender = "male" if sex == "M" else "female"
        birth_date = random_generator.Basic.random_date("1930-01-01", "2000-06-01")
        date_to_majority = datetime.datetime.strptime(birth_date, "%Y-%m-%d")
        register_day = date_to_majority + datetime.timedelta(days=6575)
        self.first_name = first_name
        self.last_name = last_name
        self.gender = gender

        self.email = random_generator.Person.email()
        while self.email in [pat.pesel for pat in Patient.list_of_patients]:
            self.email = random_generator.Person.email()

        self.pesel = random_generator.Person.pesel(sex, birth_date, True)
        while self.pesel in [pat.pesel for pat in Patient.list_of_patients]:
            self.pesel = random_generator.Person.pesel(sex, birth_date, True)

        self.date_of_register = register_day.strftime("%Y-%m-%d")
        self.blood_group = random.choices(
            population=[
                "0 Rh+",
                "A Rh+",
                "B Rh+",
                "AB Rh+",
                "0 Rh-",
                "A Rh-",
                "B Rh-",
                "AB Rh-",
            ],
            weights=[31, 32, 15, 7, 6, 6, 2, 1],
        )[0]

        self.phone_number = random_generator.Person.phone_number()
        while self.phone_number in [
            pat.phone_number for pat in Patient.list_of_patients
        ]:
            self.phone_number = random_generator.Person.phone_number()

        while self.phone_number in [
            pat.phone_number for pat in Patient.list_of_patients
        ]:
            self.phone_number = random_generator.Person.phone_number()
        Patient.list_of_patients.append(self)


class Donation:
    """
    Create Donation
    """

    list_of_patients = {}

    def __init__(self, patient):
        self.patient = patient

        if patient not in Donation.list_of_patients.keys():
            self.date_of_donation = patient.date_of_register
            accept_donate = random.choices(
                population=["True", "False"], weights=[85, 15]
            )[0]
            self.accept_donate = accept_donate
            Donation.list_of_patients[patient] = [patient.date_of_register]
        else:
            self.date_of_donation, self.accept_donate = Donation.__date_of_next_donate(
                patient
            )

        self.refuse_information = (
            None
            if self.accept_donate == "True"
            else random_generator.Basic.words(random.randint(10, 30))
        )

    @classmethod
    def __date_of_next_donate(cls, patient_to_find):
        """
        returns date of next donation or remove patient if he cannot donate
        """
        donate = Donation.list_of_patients[patient_to_find][-1]
        last_donate = datetime.datetime.strptime(donate, "%Y-%m-%d")
        if (datetime.datetime.today() - last_donate).days < 91:
            correct_date_to_donate = last_donate + datetime.timedelta(
                days=random.randint(1, (datetime.datetime.today() - last_donate).days)
            )
            Patient.list_of_patients.remove(patient_to_find)
            return correct_date_to_donate.strftime("%Y-%m-%d"), "False"
        else:
            correct_date_to_donate = last_donate + datetime.timedelta(days=90)
            date_donate = random_generator.Basic.random_date(correct_date_to_donate)
            Donation.list_of_patients[patient_to_find] += [date_donate]
            return (
                date_donate,
                random.choices(population=["True", "False"], weights=[75, 25])[0],
            )


def folder_for_data():
    """creates folder for dummy_data"""
    folder_for_data = "dummy_data"
    path_to_data = os.path.join(os.getcwd(), folder_for_data)
    try:
        os.makedirs(path_to_data)
    except FileExistsError:
        pass
    return path_to_data


def users_json(path_folder):
    """Create json file for users and saves"""
    json_info = []
    list_username = ["admin"]
    for _ in range(NUMBER_OF_USERS):
        username = random_generator.Basic.words(1)
        while username in list_username:
            username = random_generator.Basic.words(1)
        list_username += [username]
        first_name, last_name = random_generator.Person.full_name()
        json_info.append(
            {
                "username": username,
                "email": random_generator.Person.email(),
                "password": random_generator.Person.password(),
                "first_name": first_name,
                "last_name": last_name,
            }
        )
    with open(os.path.join(path_folder, "users.json"), "w") as json_file:
        json.dump(json_info, json_file)


def profile_json(path_folder):
    """Create json file for profile and saves"""
    json_info = []
    images = random_generator.Basic.image(path_folder, "hospital", 30)
    for _ in range(NUMBER_OF_USERS):
        json_info.append(
            {
                "image": random.choice(images),
                "position": random.choice(
                    [
                        "doctor",
                        "resident doctor",
                        "medical specialist",
                        "habilitated doctor",
                        "professor",
                        "nurse",
                    ]
                ),
                "branch": random.choice(
                    ["Warszawa", "Lublin", "Radom", "Gdynia", "Kraków"]
                ),
            }
        )
    with open(os.path.join(path_folder, "profile.json"), "w") as json_file:
        json.dump(json_info, json_file)


def patient_json(path_folder):
    """Create json file for patient and saves"""
    json_info = []
    for _ in range(NUMBER_OF_PATIENTS):
        patient = Patient()
        json_info.append(
            {
                "first_name": patient.first_name,
                "email": patient.email,
                "last_name": patient.last_name,
                "gender": patient.gender,
                "pesel": patient.pesel,
                "blood_group": patient.blood_group,
                "phone_number": patient.phone_number,
                "date_of_register": patient.date_of_register,
            }
        )
    with open(os.path.join(path_folder, "patient.json"), "w") as json_file:
        json.dump(json_info, json_file)


def donation_json(path_folder):
    """Create json file for donation and saves"""
    json_info = []
    for _ in range(NUMBER_OF_DONATION):
        donation = Donation(random.choice(Patient.list_of_patients))
        json_info.append(
            {
                "pesel_test": donation.patient.pesel,
                "patient_pesel": donation.patient.pesel,
                "date_of_donation": donation.date_of_donation,
                "accept_donate": donation.accept_donate,
                "refuse_information": donation.refuse_information,
            }
        )
    with open(os.path.join(path_folder, "donation.json"), "w") as json_file:
        json.dump(json_info, json_file)


print("It will take few seconds depends on amount of generated data...")
path = folder_for_data()
users_json(path)
profile_json(path)
while True:
    try:
        patient_json(path)
        donation_json(path)
        break
    except IndexError:
        print(
            "Refresh....Just Wait. "
            "If this will happen more times you need to lower NUMBER_OF_DONATION or add more to NUMBER OF PATIENTS"
        )
        Patient.list_of_patients.clear()
        Donation.list_of_patients.clear()

print(
    "\n===Open terminal in root directory and write this commands==="
    "\n\npython manage.py makemigrations && "
    "python manage.py migrate && "
    f"python manage.py populate_db {folder_for_data()} -a && "
    "python manage.py createcachetable && "
    "python manage.py runserver"
    "\n\n===LOOK TO THE TOP==="
)
