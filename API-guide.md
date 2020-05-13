# IN PROGRESS THERE IS NO CODE IN REPO YET OR ONLINE !!!!!!
> IN PROGRESS !!!!!!



| URI                                              | GET                                                 | POST                                  | PUT                               | DELETE                                      |
| ----------------------------------------------------- | --------------------------------------------------- | ------------------------------------- | --------------------------------- | ------------------------------------------- |
| [/api/v1/](#URIs_list)                             | Returns a list of links to the other available URIs | N/A                                   | N/A                               | N/A                                         |
| [/api/v1/patients/](#Patient_list)                                 | Returns a list of patients                           | Creates a new patient                  | N/A                               | N/A                                         |
| [/api/v1/patients/{id}](#Patient)                                 | Returns the details of a single patient                           |  N/A                   | Updates a patient                               | Deletes a patient                                        |
| [/api/v1/donations/](#Donations_list)                                 | Returns a list of donations                           | Creates a new donation                  | N/A                               | N/A                                         |

### URIs_list

| URI | Method   |**GET** |
| --- |  ------- |  ------- |
| `/api/v1/`  | Permission |All      |

> GET

Returns list of avalible URIs.

### Patient_list

| URI                  | Method         |**GET**     |**POST** |
| -------------------- |  ------------- |  --------- |-------- |
| `/api/v1/patients/`  | Permission     | Users      | Users   |

> GET

Returns list of Patients with all of their donations and medical employee responsible for register, also there is added dynamic field which returns information if the current Patient can donate

| Filter                | lookups           | Description |
| --------------------- | ---------------- | ----------- |
| **id**                | in           | Django’s built-in lookup |
| **first_name**          | exact, icontains           | Django’s built-in lookup |
| **last_name**         | exact, icontains           | Django’s built-in lookup |
| **pesel**          | exact, icontains           | Django’s built-in lookup |
| **blood_group**            | exact, icontains          | Django’s built-in lookup |
| **gender**      | exact          | Django’s built-in lookup |
| **email**      | exact, icontains          | Django’s built-in lookup |
| **phone_number**      | exact, icontains          | Django’s built-in lookup |
| **date_of_register**      | exact, icontains, gt, gte, lt, lte, year, month, day          | Django’s built-in lookup |
| **can_donate**      | exact          | Django’s built-in lookup |
| **registered_by**      | in          | Django’s built-in lookup |
| **search**      | icontains          | Search given value in: first_name, last_name, pesel, email, phone_number   |
| **fields**      | Selective fields          | Returns only selected fields |
| **omit**      | Selective fields          | Returns all fields except omitted ones |
| **page**      | Pagination          | Returns page |
| **page_size**      | Pagination          | Returns number of records on page (default=200, max_page_size=1000 |

Example: 

`/api/v1/patients/?page_size=100&can_donate=true&date_of_register__gte=1990-09-26&omit=registered_by&first_name__icontains=Vit`

> POST

Adds new Patient (date_of_register and registered_by are done automatically)


| Element / Attribute	 | Type         |Permission|
| -------------------- |  ------------- |----------|
|  first_name  |  String    |Required|
|  last_name |   String   |Required|
|   pesel|   Integer(BigIntegerField)   |Required|
|   blood_group|   String(chocies: 0 Rh+, A Rh+, B Rh+, AB Rh+, 0 Rh-, A Rh-, B Rh-, B Rh-)   |Required|
|   gender|  String(chocies: male, female)    |Required|
|   email|   String(EmailField)   |Allowed|
|  phone_number |  Integer(PhoneNumberField)  *should start with Country calling code like: "+48"*    |Allowed|

Example:

`{
    "first_name": "Testowy",
    "last_name": "Testowicz",
    "pesel": 12345678910,
    "blood_group": "0 Rh+",
    "gender": "male",
    "email": "test@vp.pl",
    "phone_number": "+48123456789",
}`

### Patient

| URI                  | Method         |**GET**     |**PUT** |**DELETE** |
| -------------------- |  ------------- |  --------- |-------- | ----------|
| `/api/v1/patients/{id}`  | Permission     | Users      | Users   | Admin/staff|

> GET

Returns detaiil information about Patient with all of his/her donations and medical employee responsible for register, also there is added dynamic field which returns information if the Patient can donate.

> PUT

Updates Patient.

| Element / Attribute	 | Type         |Permission|
| -------------------- |  ------------- |----------|
|  first_name  |  String    |Required|
|  last_name |   String   |Required|
|   pesel|   Integer(BigIntegerField)   |Required|
|   blood_group|   String(chocies: 0 Rh+, A Rh+, B Rh+, AB Rh+, 0 Rh-, A Rh-, B Rh-, B Rh-)   |Required|
|   gender|  String(chocies: male, female)    |Required|
|   email|   String(EmailField)   |Allowed|
|  phone_number |  Integer(PhoneNumberField)  *should start with Country calling code like: "+48"*    |Allowed|

Example:

`{
    "first_name": "ZMIANATestowy",
    "last_name": "Testowicz",
    "pesel": 12345678910,
    "blood_group": "0 Rh+",
    "gender": "male"
}`

> DELETE

Deletes Patient(only admin or staff can do it).

### Donations_list

| URI                  | Method         |**GET**     |**POST** |
| -------------------- |  ------------- |  --------- |-------- |
| `/api/v1/donations/`  | Permission     | Users      | Users   |

> GET

Returns list of Donations.

| Filter                | lookups           | Description |
| --------------------- | ---------------- | ----------- |
| **id**                | in           | Django’s built-in lookup |
| **medical_staff**         | in            | Django’s built-in lookup |
| **patient**          | in          | Django’s built-in lookup |
| **date_of_donation**            | exact, icontains, gt, gte, lt, lte, year, month, day          | Django’s built-in lookup |
| **accept_donate**      | exact          | Django’s built-in lookup |
| **refuse_information**      | icontains          | Django’s built-in lookup |
| **fields**      | Selective fields          | Returns only selected fields |
| **omit**      | Selective fields          | Returns all fields except omitted ones |
| **page**      | Pagination          | Returns page |
| **page_size**      | Pagination          | Returns number of records on page (default=250, max_page_size=2000 |

Example: 

`/api/v1/donations/?medical_staff=32,54,534,56,33,77,23,43&accept_donate=true`

> POST

Adds new Donation (date_of_donation and medical_staff are done automatically)


| Element / Attribute	 | Type         |Permission|
| -------------------- |  ------------- |----------|
|   patient|   Integer(BigIntegerField)   |Required|
|   accept_donate|  String(chocies: male, female)    |Required|
|   refuse_information|   String(EmailField)   |Allowed|

Example:

`{
    "accept_donate": "True",
    "patient": 123
}`
