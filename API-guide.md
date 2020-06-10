# REST API documentation
>  All endpoints explained

## Login

Use API as admin:

login: admin

password: admin

Token: d5c46c545a579513e88456bd8a85aee36e7a646f

## Endpoints

| URI                                              | GET                                                 | POST                                  | PUT                               | DELETE                                      |
| ----------------------------------------------------- | --------------------------------------------------- | ------------------------------------- | --------------------------------- | ------------------------------------------- |
| [/api/v1/](#URIs_list)                             | Returns a list of links to the other available URIs | N/A                                   | N/A                               | N/A                                         |
| [/api/get-token](#Token)                                 | N/A                            | Returns token for user                 | N/A                               | N/A                                         |
| [/api/v1/public/](#Public)                                 | Returns informations about current state of bloods in all branches                           | N/A                   | N/A                               | N/A                                         |
| [/api/v1/public/{branch}](#Public)                                 | Returns informations about current state of bloods in branch                           | N/A                   | N/A                               | N/A                                         |
| [/api/v1/users/](#Users)                                 | Returns a list of users                           | N/A                   | N/A                               | N/A                                         |
| [/api/v1/users/{id}](#Users)                                 | Returns a user                           | N/A                   | N/A                               | N/A                                         |
| [/api/v1/patients/](#Patients_list)                                 | Returns a list of patients                           | Creates a new patient                  | N/A                               | N/A                                         |
| [/api/v1/patients/{id}](#Patient)                                 | Returns the details of a single patient                           |  N/A                   | Updates a patient                               | Deletes a patient                                        |
| [/api/v1/donations/](#Donations_list)                                 | Returns a list of donations                           | Creates a new donation                  | N/A                               | N/A                                         |
| [/api/v1/donations/{id}](#Donation)                                 | Returns the details of a single donation                           |  N/A                   | Updates a donation                               | Deletes a donation                                        |
### URIs_list

#### Single example: 

```
{
    "patients": "https://blood-dontaion.herokuapp.com/api/v1/patients/",
    "donations": "https://blood-dontaion.herokuapp.com/api/v1/donations/",
    "users": "https://blood-dontaion.herokuapp.com/api/v1/users/",
    "public": "https://blood-dontaion.herokuapp.com/api/v1/public/"
}
```

| URI | Method   |**GET** |
| --- |  ------- |  ------- |
| `/api/v1/`  | Permission |All      |

> GET

Returns list of avalible URIs.

### Token

#### Single example: 

```
{
    "token": "dee9a966e4fe39abf1e59b9e950d28632e4454f6"
}
```

#### Permissible Fields

| Element / Attribute     | POST       |  
| ----------------------- | --------- | 
| **username**                    | Required  | 
| **password**              | Required   |

| URI | Method   |**POST** |
| --- |  ------- |  ------- |
| `/api/get-token`  | Permission |All      |

> POST

Returns token for user.

### Public

#### Single example: 

```
{
    "Branch": "Lublin",
    "percentage_blood_share": {
        "A Rh+": 34.69,
        ...
        "B Rh-": 0.86
    },
    "state_of_blood_supply": {
        "A Rh+": 100,
        ...
        "B Rh-": 6.88
    }
}
```

| URI | Method   |**GET** |
| --- |  ------- |  ------- |
| `/api/v1/public/`  | Permission |All      |

> GET

Returns informations about current state of bloods in all branches.

| URI | Method   |**GET** |
| --- |  ------- |  ------- |
| `/api/v1/public/{branch}`  | Permission |All      |

> GET

Returns informations about current state of bloods in branch.

### Users

#### Single example: 

```
{
    "id": 12,
    "username": "c",
    "first_name": "Amine",
    "last_name": "Rutkowski",
    "email": "dtzfawwbd@123mail.cl",
    "position": "habilitated doctor",
    "branch": "Radom",
    "image": "https://blood-donation-live.s3.eu-west-2.amazonaws.com/profile_image/c.jpg?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIAVGRKEV6O54SLRAVI%2F20200609%2Feu-west-2%2Fs3%2Faws4_request&X-Amz-Date=20200609T125348Z&X-Amz-Expires=3600&X-Amz-SignedHeaders=host&X-Amz-Signature=c5fdf899436a2e178ed70742d1b7c81929e445a333bd8a22afdf57ee17873919"
}
```

#### Sortable Fields

| Filter                | Type | lookups           | Description |
| --------------------- | --|---------------- | ----------- |
| **search**                | String| SearchFilter           | Search given value in: username, last_name, email, branch  |
| **fields**      | String|Selective fields          | Returns only selected fields |
| **omit**      | String|Selective fields          | Returns all fields except omitted ones |
| **page**      |Integer |Pagination          | Returns page |
| **page_size**      | Integer|Pagination          | Returns number of records on page (default=50, max_page_size=500 |


| URI                  | Method         |**GET**     |
| -------------------- |  ------------- |  --------- |
| `/api/v1/users/`  | Permission     | Users      | 

> GET

Returns list of users with branch, position and image.

| URI | Method   |**GET** |
| --- |  ------- |  ------- |
| `/api/v1/users/{id}`  | Permission |Users      |

> GET

Returns informations about user.







### Patients_list

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
|   blood_group|   String(chocies: 0 Rh+, A Rh+, B Rh+, AB Rh+, 0 Rh-, A Rh-, B Rh-, AB Rh-)   |Required|
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

Deletes Patient.

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

### Donation

| URI                  | Method         |**GET**     |**PUT** |**DELETE** |
| -------------------- |  ------------- |  --------- |-------- | ----------|
| `/api/v1/donations/{id}`  | Permission     | Users      | Admin/staff   | Admin/staff|

> GET

Returns detaiil information about Donation, patient and medical employee.

> PUT

Updates Donation.

| Element / Attribute	 | Type         |Permission|
| -------------------- |  ------------- |----------|
|   patient|   Integer(BigIntegerField)   |Required|
|   accept_donate|  String(chocies: male, female)    |Required|
|   refuse_information|   String(EmailField)   |Allowed|

Example:

`{
    "accept_donate": "False",
    "patient": 123,
    "refuse_information": "Because I say so"
}`

> DELETE

Deletes Donation.

