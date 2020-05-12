# IN PROGRESS THERE IS NO CODE IN REPO YET OR ONLINE !!!!!!
> IN PROGRESS !!!!!!



| URI                                              | GET                                                 | POST                                  | PUT                               | DELETE                                      |
| ----------------------------------------------------- | --------------------------------------------------- | ------------------------------------- | --------------------------------- | ------------------------------------------- |
| [/api/v1/](#URIs_list)                             | Returns a list of links to the other available URIs | N/A                                   | N/A                               | N/A                                         |
| [/api/v1/patients/](#Patient_list)                                 | Returns a list of patients                           | Creates a new patient                  | N/A                               | N/A                                         |


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
| **search**      | custom          | Search given value in: first_name, last_name, pesel, email, phone_number   |
| **fields**      | Selective fields          | Returns only selected fields |
| **omit**      | Selective fields          | Returns all fields except omitted ones |
